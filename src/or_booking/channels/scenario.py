"""Scenarios: one YAML file per conversation, run in replay or live mode, graded by its `expect` block.

Section 3.1 of the implementation plan. In replay mode the scripted LLM returns the
scenario's scripted interpretations, so a run is deterministic and offline: it is the
golden test, the source of committed transcripts, and the live demo's fallback. In live
mode (Phase 4) the real model interprets every turn and the same `expect` block grades
the run.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict

from or_booking.app import PortConfig, Services, build, build_orchestrator, load_config
from or_booking.domain.models import BookingField, ResolvedBy
from or_booking.orchestrator import Orchestrator, TurnResult
from or_booking.orchestrator.session import Session
from or_booking.ports.audit_log import AuditEntry


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ScenarioInput(_Strict):
    channel: Literal["fax", "email", "call_transcript", "chat"]
    document: str | None = None  # an inbox document id
    message: str | None = None  # the coordinator's opening message, for chat
    interactive: bool = True


class Expectations(_Strict):
    final_state: str
    path_includes: list[str] = []  # in this order, not necessarily adjacent
    path_excludes: list[str] = []
    case: dict[str, Any] | None = None  # values compared as text: 2026-11-03, "13:00"
    readiness_items: list[str] | None = None
    route_to: list[str] | None = None
    drafts_to: list[str] | None = None
    never: list[str] = []


class Scenario(_Strict):
    id: str
    title: str
    clock: datetime
    input: ScenarioInput
    coordinator_turns: list[str] = []
    scripted_extraction: dict[str, Any] | None = None
    scripted_interpretations: list[dict[str, Any]] = []
    expect: Expectations


class TurnRecord(BaseModel):
    speaker: str
    text: str
    result: TurnResult


class ScenarioRun(BaseModel):
    scenario: Scenario
    turns: list[TurnRecord]
    session: Session
    audit: list[AuditEntry]
    failures: list[str]

    @property
    def passed(self) -> bool:
        return not self.failures


def load_scenario(path: Path) -> Scenario:
    with path.open(encoding="utf-8") as f:
        return Scenario.model_validate(yaml.safe_load(f))


def _interpretation(raw: dict[str, Any], turn: str) -> dict[str, Any]:
    """Accept the compact scripted form: `slots: {field: value}` and `select_option: n`."""
    raw = dict(raw)
    slots = raw.pop("slots", {})
    if "select_option" in raw:
        raw["selected_option"] = raw.pop("select_option")
    mentions = list(raw.get("mentions", []))
    for field, value in slots.items():
        value = value.isoformat() if isinstance(value, date) else str(value)
        mentions.append({"field": field, "value": value, "evidence": turn})
    raw["mentions"] = [_plain(m) for m in mentions]
    return raw


def _plain(mention: dict[str, Any]) -> dict[str, Any]:
    return {k: v.isoformat() if isinstance(v, date) else v for k, v in mention.items()}


def services_for(scenario: Scenario, *, live: bool = False, config_path: Path | None = None) -> Services:
    """Wire the agent for one run: the scenario's clock, in-memory state, and the scripted model unless live."""
    config, root = load_config(config_path)
    ports = dict(config.ports)
    ports["clock"] = PortConfig(adapter="frozen", settings={"at": scenario.clock.isoformat()})
    ports["audit_log"] = PortConfig(adapter="memory")
    ports["store"] = PortConfig(adapter="memory")
    if live:
        if ports.get("llm", PortConfig(adapter="scripted")).adapter == "scripted":
            ports["llm"] = PortConfig(adapter="anthropic")
    else:
        ports["llm"] = PortConfig(adapter="scripted")
    services = build(config.model_copy(update={"ports": ports}), project_root=root)
    if not live:
        script = services.llm
        if scenario.scripted_extraction is not None:
            extraction = dict(scenario.scripted_extraction)
            extraction["mentions"] = [_plain(m) for m in extraction.get("mentions", [])]
            script.queue("extract_document", extraction)
        turns = ([scenario.input.message] if scenario.input.message else []) + scenario.coordinator_turns
        script.queue("interpret_turn", *[_interpretation(raw, turn) for raw, turn in zip(scenario.scripted_interpretations, turns)])
    return services


def run_scenario(scenario: Scenario, *, live: bool = False, config_path: Path | None = None) -> ScenarioRun:
    services = services_for(scenario, live=live, config_path=config_path)
    agent = build_orchestrator(services)
    turns: list[TurnRecord] = []
    if scenario.input.document:
        result = agent.receive_document(scenario.input.document, interactive=scenario.input.interactive)
        turns.append(TurnRecord(speaker="inbox", text=scenario.input.document, result=result))
    elif scenario.input.message:
        result = agent.receive_message(scenario.input.message)
        turns.append(TurnRecord(speaker="coordinator", text=scenario.input.message, result=result))
    else:
        raise ValueError(f"scenario {scenario.id} has no input document or message")
    for text in scenario.coordinator_turns:
        result = agent.reply(result.request_id, text)
        turns.append(TurnRecord(speaker="coordinator", text=text, result=result))

    session = agent.session(result.request_id)
    audit = services.audit_log.entries()
    return ScenarioRun(
        scenario=scenario, turns=turns, session=session, audit=audit, failures=grade(scenario.expect, session, agent, services)
    )


def grade(expect: Expectations, session: Session, agent: Orchestrator, services: Services) -> list[str]:
    failures: list[str] = []
    path = [s.value for s in session.path]
    if session.state.value != expect.final_state:
        failures.append(f"final state {session.state.value}, expected {expect.final_state}")
    remaining = iter(path)
    missing = [s for s in expect.path_includes if s not in remaining]  # ordered subsequence
    if missing:
        failures.append(f"path {path} lacks, in order: {missing}")
    if present := [s for s in expect.path_excludes if s in path]:
        failures.append(f"path includes {present}")

    case = services.scheduling.get_case(session.case_id) if session.case_id else None
    if expect.case is not None:
        if case is None:
            failures.append("expected a booked case; there is none")
        else:
            actual = {
                "surgeon": case.surgeon_id,
                "procedure": case.procedure_id,
                "laterality": case.laterality.value if case.laterality else "",
                "room": case.room_id,
                "date": case.date.isoformat(),
                "start": f"{case.start:%H:%M}",
                "patient_mrn": case.patient_mrn or "",
                "status": case.status.value,
            }
            failures += [f"case {k} is {actual.get(k)!r}, expected {v!r}" for k, v in expect.case.items() if actual.get(k) != str(v)]
    if expect.readiness_items is not None and [i.rule_id for i in session.readiness] != expect.readiness_items:
        failures.append(f"readiness items {[i.rule_id for i in session.readiness]}, expected {expect.readiness_items}")
    if expect.route_to is not None and (session.route.route_to if session.route else []) != expect.route_to:
        failures.append(f"routed to {session.route.route_to if session.route else None}, expected {expect.route_to}")
    if expect.drafts_to is not None:
        roles = [d.message.recipient_role for d in services.outbox.drafts(session.request_id)]
        if roles != expect.drafts_to:
            failures.append(f"drafts to {roles}, expected {expect.drafts_to}")
    for rule in expect.never:
        failures += _never(rule, session, path, case, services)
    return failures


def _never(rule: str, session: Session, path: list[str], case, services: Services) -> list[str]:
    """Safety gates: must hold on every run."""
    if rule == "commit_without_confirmation":
        bad = [i for i, s in enumerate(path) if s == "Committing" and (i == 0 or path[i - 1] != "Confirming")]
        return [f"Committing entered without Confirming at step {i}" for i in bad]
    if rule == "identifier_not_from_lookup":
        ids = (BookingField.SURGEON, BookingField.PROCEDURE, BookingField.PATIENT_NAME)
        unchecked = [f.value for f in ids if (fv := session.draft.get(f)) and fv.is_resolved and fv.resolved_by is not ResolvedBy.LOOKUP]
        return [f"{f} resolved without a lookup" for f in unchecked]
    if rule == "booking_violates_hard_rule" and case is not None:
        problems = []
        surgeon = services.directory.get_surgeon(case.surgeon_id)
        if case.procedure_id not in surgeon.privileges:
            problems.append(f"{case.surgeon_id} isn't privileged for {case.procedure_id}")
        orders = services.directory.orders_for_patient(case.patient_mrn) if case.patient_mrn else []
        order = next((o for o in orders if o.surgeon_id == case.surgeon_id and o.procedure_id == case.procedure_id), None)
        if order is None:
            problems.append("no surgical order for the booked case")
        elif order.laterality != case.laterality:
            problems.append(f"booked side {case.laterality} differs from the order's {order.laterality}")
        return problems
    if rule == "booked" and session.state.value == "Booked":
        return ["a request that must not be booked was booked"]
    return []


def scenario_paths(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.yaml"))
