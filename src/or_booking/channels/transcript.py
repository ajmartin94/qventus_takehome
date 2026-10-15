"""Markdown transcripts of scenario runs, for reviewers reading the repository (docs/demo/).

A transcript shows the input, the conversation with its cards and state trace, what the
model returned, every port call, the drafted messages and the expectations checked.
Replay transcripts are deterministic and committed; a test fails if they drift from the
code. Live transcripts are snapshots of the real model's wording.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from or_booking.channels.scenario import ScenarioRun, load_scenario, run_scenario, scenario_paths
from or_booking.domain.models import ReadinessItem
from or_booking.orchestrator.cards import AnswerCard, Card, ConfirmationCard, HandoffCard, OptionsCard, OutcomeCard
from or_booking.ports.audit_log import AuditEntry, AuditKind


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _table(header: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(_cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def _readiness(items: list[ReadinessItem]) -> str:
    rows = []
    for i in items:
        due = f"{i.due:%a %b %d %H:%M}" if i.due else (f"dated {i.valid_from:%b %d} or later" if i.valid_from else "-")
        rows.append([i.item, i.owner, due, i.status.value, i.detail or ""])
    return "**Readiness list (handed off)**\n\n" + _table(["Item", "Owner", "Due", "Status", "Note"], rows)


def card_markdown(card: Card) -> str:
    if isinstance(card, OptionsCard):
        rows = [
            [o.number, o.day, o.room, o.window, o.ownership + (" (counts toward block)" if o.counts_toward_block else ""), o.fit,
             o.days_until_surgery, "; ".join(o.readiness_risks) or "none"]
            for o in card.options
        ]  # fmt: skip
        parts = [f"**{card.title}**", "", _table(["#", "Day", "Room", "Window", "Ownership", "Fit", "Days out", "Readiness risk"], rows),
                 "", f"_{card.sizing}_"]  # fmt: skip
        if card.still_needed:
            parts += ["", "Still needed to book: " + "; ".join(card.still_needed)]
        return "\n".join(parts)
    if isinstance(card, ConfirmationCard):
        rows = [[r.field, r.value, r.source] for r in card.rows]
        footer = "  \n".join(x for x in [f"Hold expires {card.hold_expires}" if card.hold_expires else "", card.straight_through] if x)
        return "\n".join([f"**{card.title}**", "", card.slot, "", _table(["Field", "Value", "Source"], rows), "", footer])
    if isinstance(card, OutcomeCard):
        parts = [f"**{card.title}**", "", _table(["", ""], [list(r) for r in card.rows])]
        if card.readiness:
            parts += ["", _readiness(card.readiness)]
        parts += ["", *[f"- Draft: {d}" for d in card.drafts]] if card.drafts else []
        return "\n".join(parts)
    if isinstance(card, HandoffCard):
        rows = [["Reason", card.reason], ["Action", card.action], ["Policy", card.policy], *[list(f) for f in card.fields]]
        return "\n".join([f"**{card.title}**", "", _table(["", ""], rows)])
    if isinstance(card, AnswerCard):
        parts = [f"**{card.title}**", "", _table(["", ""], [list(r) for r in card.rows])]
        if card.readiness:
            parts += ["", _readiness(card.readiness)]
        return "\n".join(parts)
    raise TypeError(f"unknown card {card!r}")


def _brief(entry: AuditEntry) -> str:
    """One line on what a port call did."""
    d = entry.detail
    if "error" in d:
        return f"**{d['error']['code']}**: {d['error']['message']}"
    result = d.get("result")
    args = d.get("args", [])
    if isinstance(result, dict) and "count" in result and len(result) == 1:
        return f"{result['count']} found" + (f" for {args[0]!r}" if args and isinstance(args[0], str) else "")
    if isinstance(result, dict):
        if "options" in result:
            return f"{len(result['options'])} bookable, {len(result['held'])} in other owners' blocks"
        for key in ("case_id", "hold_id", "draft_id", "handoff_id"):
            if key in result:
                extra = f" ({result['status']})" if key == "case_id" and "status" in result else ""
                return f"{result[key]}{extra}"
        if "id" in result:
            return str(result["id"])
        if "booking" in result:
            return "policies loaded"
    if isinstance(result, str):
        return result
    return ", ".join(str(a) for a in args if isinstance(a, str)) or "-"


def _model_calls(audit: list[AuditEntry], live: bool) -> str:
    lines = []
    for e in audit:
        if e.kind is not AuditKind.MODEL_CALL:
            continue
        d = e.detail
        usage = d.get("usage") or {}
        tokens = f", {usage.get('input_tokens', 0) + usage.get('cache_read_tokens', 0) + usage.get('cache_write_tokens', 0)} in / {usage.get('output_tokens', 0)} out" if live and usage else ""
        lines.append(f"**{d['prompt']}** {d['version']} (effort {d['effort']}, outcome {d['outcome']}{tokens})")
        output = d.get("output")
        if not output:
            lines.append("")
            continue
        summary = [f"intent `{output.get('intent')}`"]
        if output.get("selected_option"):
            summary.append(f"selected option {output['selected_option']}")
        if output.get("stated_urgency", "none") != "none":
            summary.append(f"urgency {output['stated_urgency']}")
        lines.append("- " + ", ".join(summary))
        mentions = output.get("mentions", []) + output.get("corrections", [])
        if mentions:
            lines += ["", _table(["Field", "Value", "Evidence"], [[m["field"], m["value"], m["evidence"]] for m in mentions])]
        unclear = output.get("unclear") or output.get("unreadable") or []
        lines += [f"- Couldn't interpret: {u}" for u in unclear]
        lines.append("")
    return "\n".join(lines)


def render(run: ScenarioRun) -> str:
    sc, live, input_text = run.scenario, run.live, run.input_text
    mode = "live: the real model read and interpreted every turn" if live else "replay: scripted model, deterministic, no network"
    parts = [
        f"# {sc.title}",
        "",
        f"Scenario `{sc.id}` · clock {sc.clock:%a %b %d %Y %H:%M} · {mode}.",
        "",
        "_Generated by `or-booking transcripts`" + (" --live" if live else "") + " from "
        "`scenarios/demo/`. Don't edit by hand._",
        "",
        f"**Result: {'PASS' if run.passed else 'FAIL'}.** Ended in **{run.session.state.value}**"
        + ("; every expectation and safety gate held." if run.passed else ": " + "; ".join(run.failures)),
        "",
        "Path: " + " → ".join(s.value for s in run.session.path),
        "",
    ]
    if input_text:
        parts += ["## The input", "", f"`{sc.input.document}` ({sc.input.channel})", "", "```text", input_text.rstrip(), "```", ""]

    parts += ["## Conversation", ""]
    for n, turn in enumerate(run.turns, start=1):
        who = {"inbox": "Inbox", "coordinator": "Coordinator", "simulation": "Simulation"}[turn.speaker]
        parts += [f"### {n}. {who}: {turn.text if turn.speaker != 'inbox' else turn.text + ' arrives'}", ""]
        if turn.result is None:
            continue
        trace = " → ".join(s.value for s in turn.result.trace) or f"stays in {turn.result.state.value}"
        parts += [f"State: {trace}" + (" (waiting)" if turn.result.waiting else ""), ""]
        if turn.result.reply.message:
            parts += ["> " + turn.result.reply.message.replace("\n", "\n>\n> "), ""]
        for card in turn.result.reply.cards:
            parts += [card_markdown(card), ""]

    parts += ["## What the model returned", ""]
    if not live:
        parts += ["_Replay mode: these outputs are the scenario's scripted interpretations, recorded the same way live calls are._", ""]
    parts += [_model_calls(run.audit, live)]

    calls = [e for e in run.audit if e.kind is AuditKind.PORT_CALL]
    parts += ["## Port calls", "", _table(["#", "Request", "Call", "Outcome"], [[i, e.request_id or "-", e.name, _brief(e)] for i, e in enumerate(calls, 1)]), ""]

    drafts = run.drafts
    if drafts:
        parts += ["## Drafted messages (not sent)", ""]
        for d in drafts:
            m = d.message
            to = m.recipient.name if m.recipient else m.recipient_role.replace("_", " ")
            parts += [f"**{d.draft_id}: {m.subject}** to {to} ({m.channel.value})", "", "```text", m.body.rstrip() or "(empty)", "```", ""]

    counts = {k: sum(1 for e in run.audit if e.kind is k) for k in AuditKind}

    def n(kind: AuditKind, noun: str) -> str:
        return f"{counts[kind]} {noun}{'' if counts[kind] == 1 else 's'}"

    parts += [
        "## Audit trail",
        "",
        f"{n(AuditKind.TRANSITION, 'transition')}, {n(AuditKind.MODEL_CALL, 'model call')}, "
        f"{n(AuditKind.PORT_CALL, 'port call')} and {n(AuditKind.DECISION, 'recorded decision')}.",
        "",
        "## Expectations checked",
        "",
        *[f"- {line}" for line in _expectations(run)],
        "",
    ]
    return "\n".join(parts)


def demo_transcripts(scenario_dir: Path, out_dir: Path) -> dict[Path, str]:
    """Every replay transcript, plus the index (which also links any live snapshots already in out_dir/live)."""
    pages: dict[Path, str] = {}
    rows = []
    for path in scenario_paths(scenario_dir):
        run = run_scenario(load_scenario(path))
        pages[out_dir / f"{path.stem}.md"] = render(run)
        live = out_dir / "live" / f"{path.stem}.md"
        rows.append([f"[{path.stem.split('_')[0].upper()}]({path.stem}.md)", run.scenario.title, run.session.state.value,
                     "pass" if run.passed else "FAIL", f"[live run](live/{path.stem}.md)" if live.exists() else "-"])  # fmt: skip
    pages[out_dir / "README.md"] = "\n".join(
        [
            "# Demo transcripts",
            "",
            "Each demo scenario in `scenarios/demo/`, run end to end and written out: the input, the conversation with its "
            "cards and state trace, what the model returned, every port call, the drafted messages and the checks that held.",
            "",
            "Replay transcripts use the scripted model, so they are deterministic; a test fails if they drift from the code. "
            "Live transcripts are snapshots of runs with the real model reading and interpreting every turn, so their wording "
            "is the model's and varies between runs.",
            "",
            "Regenerate with `or-booking transcripts` (add `--live d1` to refresh a live snapshot; that spends API credit).",
            "",
            _table(["Scenario", "Title", "Ends in", "Replay", "Live"], rows),
            "",
        ]
    )
    return pages


def _expectations(run: ScenarioRun) -> list[str]:
    e = run.scenario.expect
    lines = [f"Final state is {e.final_state}"]
    if e.path_includes:
        lines.append("Path includes, in order: " + " → ".join(e.path_includes))
    if e.path_excludes:
        lines.append("Path never enters: " + ", ".join(e.path_excludes))
    if e.case:
        lines.append("Booked case: " + ", ".join(f"{k} {v}" for k, v in e.case.items()))
    if e.readiness_items:
        lines.append("Readiness items: " + ", ".join(e.readiness_items))
    if e.route_to:
        lines.append("Routed to: " + ", ".join(e.route_to))
    if e.drafts_to:
        lines.append("Drafts to: " + ", ".join(e.drafts_to))
    if e.asked_about:
        lines.append("Questions asked: " + ", ".join(e.asked_about))
    lines += [f"A reply says: {t!r}" for t in e.replies_include]
    if e.booked_cases_for_patient is not None:
        lines.append(f"Booked cases for the patient: {e.booked_cases_for_patient}")
    gates = {
        "commit_without_confirmation": "Nothing committed without passing through confirmation",
        "identifier_not_from_lookup": "Every identifier came from a lookup",
        "booking_violates_hard_rule": "The booking breaks no hard rule (privileges, surgeon's order, side)",
        "booked": "Nothing was booked",
    }
    lines += [f"Safety gate: {gates.get(rule, rule)}" for rule in e.never]
    return lines
