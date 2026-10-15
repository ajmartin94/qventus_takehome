"""Command-line channel. Builds the services through the composition root and renders with Rich.

Commands:
- `ports`: how each port is wired.
- `availability` and `schedule`: raw views of the scheduling service, for checking the
  simulated hospital.
- `replay`: run a scenario with the scripted model, deterministic and offline.
- `chat`: talk to the agent; with `--scenario`, step through a scripted conversation.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from or_booking.app import PORTS, PortConfig, Services, build, build_orchestrator, load_config
from or_booking.channels.render import render_result
from or_booking.channels.scenario import load_scenario, run_scenario, scenario_paths, services_for
from or_booking.domain.errors import BookingError
from or_booking.domain.models import AvailabilityQuery, BookingField, CaseMinutes, DateWindow, SlotOption
from or_booking.orchestrator import Orchestrator
from or_booking.orchestrator.states import WAITING
from or_booking.ports.event_source import EventType, ScheduleEvent

app = typer.Typer(no_args_is_help=True, add_completion=False, help="AI-assisted OR case booking (prototype).")
console = Console()

_STATE_STYLE = {"held": "blue", "released": "green", "open": "white"}
SCENARIO_DIR = Path("scenarios/demo")


def _services() -> Services:
    return build()


@app.callback()
def main() -> None:
    """AI-assisted OR case booking (prototype)."""


# ---------------------------------------------------------------------------
# The simulated hospital
# ---------------------------------------------------------------------------


@app.command()
def ports() -> None:
    """Show every port and the adapter wired to it."""
    services = _services()
    table = Table(title="Ports and adapters", title_justify="left")
    table.add_column("Port", style="bold")
    table.add_column("Adapter")
    table.add_column("Recorded")
    table.add_column("Responsibility")
    for spec in PORTS:
        adapter = services.wiring[spec.name]
        table.add_row(
            spec.name,
            adapter if adapter != "-" else "[dim]not wired yet[/dim]",
            "yes" if spec.audited else "",
            spec.summary,
        )
    console.print(table)
    console.print(f"Clock: {services.clock.now():%a %b %d %Y %H:%M}")


@app.command()
def availability(
    surgeon: str = typer.Option("S-PATEL", help="Surgeon id"),
    procedure: str = typer.Option("TKA-ROBOTIC", help="Procedure id"),
    typical: int = typer.Option(112, help="Typical (P50) case minutes"),
    long: int = typer.Option(135, help="Long (P80) case minutes"),
    start: str = typer.Option("2026-11-02", help="First date (YYYY-MM-DD)"),
    end: str = typer.Option("2026-11-06", help="Last date (YYYY-MM-DD)"),
) -> None:
    """Send an availability query to the scheduling service. Defaults are scenario D1."""
    services = _services()
    query = AvailabilityQuery(
        surgeon_id=surgeon,
        procedure_id=procedure,
        case_minutes=CaseMinutes(typical=typical, long=long),
        window=DateWindow(start=date.fromisoformat(start), end=date.fromisoformat(end)),
    )
    try:
        result = services.scheduling.search_availability(query)
    except BookingError as err:
        console.print(f"[red]{err.code}[/red]: {err.message}")
        raise typer.Exit(1) from err

    console.print(f"[bold]Availability query[/bold] {query.model_dump_json()}")
    console.print(_options_table("Bookable options", result.options))
    console.print(_options_table("In another owner's unreleased block", result.held))
    if result.closed_dates:
        console.print("Schedule closed (add-ons): " + ", ".join(f"{d:%a %b %d}" for d in result.closed_dates))


def _options_table(title: str, options: list[SlotOption]) -> Table:
    table = Table(title=title, title_justify="left")
    for column in ("Option", "Day", "Room", "Window", "Fits up to", "Ownership", "Owner", "Release"):
        table.add_column(column)
    for o in options:
        release = o.releases_at or o.released_at
        table.add_row(
            o.option_id,
            f"{o.start:%a %b %d}",
            o.room_id,
            f"{o.start:%H:%M}-{o.end:%H:%M} ({o.window_minutes} min)",
            f"{o.case_capacity_minutes} min",
            o.ownership.value,
            o.block_owner_name or "",
            ("releases " if o.releases_at else "released ") + f"{release:%b %d %H:%M}" if release else "",
        )
    return table


@app.command()
def schedule(
    start: str = typer.Option("2026-11-02", help="First date (YYYY-MM-DD)"),
    end: str = typer.Option("2026-11-06", help="Last date (YYYY-MM-DD)"),
) -> None:
    """Show the OR schedule: rooms by day, block owners colored by release state, booked cases."""
    console.print(schedule_table(_services(), date.fromisoformat(start), date.fromisoformat(end)))


def schedule_table(services: Services, start: date, end: date) -> Table:
    view = services.scheduling.get_schedule(DateWindow(start=start, end=end))
    days = sorted({rd.date for rd in view.room_days})
    table = Table(title="OR schedule  [blue]held block[/blue]  [green]released[/green]  open  [dim]filler[/dim]", title_justify="left")
    table.add_column("Room", style="bold")
    for d in days:
        table.add_column(f"{d:%a %b %d}")
    for room in sorted({rd.room_id for rd in view.room_days}):
        cells = []
        for d in days:
            rd = next(r for r in view.room_days if r.room_id == room and r.date == d)
            if rd.fully_booked:
                cells.append("[dim]booked[/dim]")
                continue
            lines = []
            for seg in rd.segments:
                owner = seg.owner_name or "open time"
                if seg.filler:
                    lines.append(f"[dim]{owner} (booked)[/dim]")
                else:
                    lines.append(f"[{_STATE_STYLE[seg.state]}]{seg.start:%H:%M} {owner}[/{_STATE_STYLE[seg.state]}]")
            lines += [f"  {c.start:%H:%M}-{c.end:%H:%M} {c.procedure_id}" for c in rd.cases]
            cells.append("\n".join(lines))
        table.add_row(room, *cells)
    return table


# ---------------------------------------------------------------------------
# Talking to the agent
# ---------------------------------------------------------------------------


def find_scenario(name: str) -> Path:
    """A path, or a demo scenario's file name or prefix: 'd1' finds scenarios/demo/d1_faxed_request.yaml."""
    path = Path(name)
    if path.exists():
        return path
    folder = load_config()[1] / SCENARIO_DIR
    matches = [p for p in scenario_paths(folder) if p.stem == name or p.stem.startswith(f"{name}_")]
    if len(matches) != 1:
        raise typer.BadParameter(f"{len(matches)} scenarios match {name!r} in {folder}")
    return matches[0]


@app.command()
def replay(
    scenario: str = typer.Argument(..., help="Scenario file, or a demo scenario name such as d1"),
    live: bool = typer.Option(False, "--live", help="Let the real model read and interpret every turn (spends API credit)"),
) -> None:
    """Run a scenario and grade it against its expectations. Scripted model by default: deterministic, no network."""
    sc = load_scenario(find_scenario(scenario))
    run = run_scenario(sc, live=live)
    mode = "live model" if live else "scripted model"
    console.rule(f"[bold]{sc.title}[/bold]  ({sc.id}, clock {sc.clock:%a %b %d %H:%M}, {mode})")
    for turn in run.turns:
        style = "yellow" if turn.speaker == "simulation" else "magenta"
        console.print(Text(f"{turn.speaker}: {turn.text}", style=style))
        if turn.result:
            console.print(render_result(turn.result))
        console.print()
    if live:
        console.print(Text(_model_usage(run.audit), style="dim"))
    if run.passed:
        console.print(Text(f"PASS: {sc.id} ended in {run.session.state.value}; every expectation and safety gate held.", style="green"))
        return
    for failure in run.failures:
        console.print(Text(f"FAIL: {failure}", style="red"))
    raise typer.Exit(1)


def _model_usage(audit: list) -> str:
    calls = [e for e in audit if e.kind.value == "model_call"]
    usage = [e.detail.get("usage", {}) for e in calls]
    tokens_in = sum(u.get("input_tokens", 0) + u.get("cache_read_tokens", 0) + u.get("cache_write_tokens", 0) for u in usage)
    tokens_out = sum(u.get("output_tokens", 0) for u in usage)
    served = sorted({e.detail.get("served_by") for e in calls if e.detail.get("served_by")})
    return f"{len(calls)} model calls, {tokens_in} input / {tokens_out} output tokens, served by {', '.join(served) or '-'}"


def _live_services() -> Services:
    config, root = load_config()
    ports = {**config.ports, "llm": PortConfig(adapter="anthropic")}
    return build(config.model_copy(update={"ports": ports}), project_root=root)


@app.command()
def chat(
    scenario: str = typer.Option(None, help="Start from a scenario's input; press Enter to send its next coordinator turn"),
    live: bool = typer.Option(False, "--live", help="Use the real model, so you can type freely (spends API credit)"),
    coordinator: str = typer.Option("C-0042", help="Who confirms bookings in this session"),
) -> None:
    """Talk to the agent. Type /help for commands."""
    turns: list[str] = []
    current: str | None = None
    if scenario:
        sc = load_scenario(find_scenario(scenario))
        services = services_for(sc, live=live)
        agent = build_orchestrator(services, coordinator_id=coordinator)
        turns = list(sc.coordinator_turns)
        if sc.input.document:
            console.print(Text(f"inbox: {sc.input.document}", style="magenta"))
            result = agent.receive_document(sc.input.document, interactive=sc.input.interactive)
        else:
            console.print(Text(f"coordinator: {sc.input.message}", style="magenta"))
            result = agent.receive_message(sc.input.message or "")
        console.print(render_result(result))
        current = result.request_id
    else:
        services = _live_services() if live else _services()
        if services.wiring.get("llm") == "scripted":
            console.print("Free chat needs the live model: add --live (and ANTHROPIC_API_KEY in .env), or use --scenario.")
            raise typer.Exit(1)
        agent = build_orchestrator(services, coordinator_id=coordinator)

    while True:
        hint = f" [dim](Enter sends: {turns[0]})[/dim]" if turns else ""
        try:
            line = console.input(f"[bold]{current or 'new'}>[/bold]{hint} ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line and turns:
            line = turns.pop(0)
            console.print(Text(f"coordinator: {line}", style="magenta"))
        if not line:
            continue
        if line.startswith("/"):
            if line.split()[0] in ("/quit", "/exit", "/q"):
                break
            current = _command(line, agent, services, current)
            continue
        waiting = current is not None and agent.session(current).state in WAITING
        result = agent.reply(current, line) if waiting and current else agent.receive_message(line)
        current = result.request_id
        console.print(render_result(result))


_HELP = """/inbox                       list inbox documents
/open <doc> [unattended]     start a request from a document
/sessions                    list requests          /switch <REQ-id>  talk about another request
/event displaced <case-id>   simulate a displaced case
/tick                        run timers (reply deadlines)
/schedule [start end]        the OR schedule        /drafts  outbox drafts
/audit                       this request's audit trail
/quit"""


def _command(line: str, agent: Orchestrator, services: Services, current: str | None) -> str | None:
    name, *args = line[1:].split()
    if name == "help":
        console.print(_HELP)
    elif name == "inbox":
        for doc in services.document_ingest.list_documents():
            console.print(f"{doc.document_id:10} {doc.channel.value:16} {doc.received_at:%H:%M}  {doc.sender or ''}")
    elif name == "open" and args:
        result = agent.receive_document(args[0], interactive=not (len(args) > 1 and args[1] == "unattended"))
        console.print(render_result(result))
        return result.request_id
    elif name == "sessions":
        table = Table(title="Requests", title_justify="left")
        for column in ("Request", "State", "Kind", "Patient", "Procedure", "Case"):
            table.add_column(column)
        for s in agent.sessions():
            patient, procedure = s.draft.get(BookingField.PATIENT_NAME), s.draft.get(BookingField.PROCEDURE)
            table.add_row(
                s.request_id, s.state.value, s.kind.value, patient.stated if patient else "", procedure.stated if procedure else "", s.case_id or ""
            )
        console.print(table)
    elif name == "switch" and args:
        return args[0]
    elif name == "event" and len(args) == 2 and args[0] == "displaced":
        event = ScheduleEvent(event_id=f"E-{args[1]}", type=EventType.CASE_DISPLACED, occurred_at=services.clock.now(), case_ids=[args[1]])
        services.event_source.inject(event)
        results = agent.process_events()
        for result in results:
            console.print(render_result(result))
        return results[-1].request_id if results else current
    elif name == "tick":
        for result in agent.tick():
            console.print(render_result(result))
    elif name == "schedule":
        start, end = (date.fromisoformat(a) for a in args) if len(args) == 2 else (date(2026, 11, 2), date(2026, 11, 6))
        console.print(schedule_table(services, start, end))
    elif name == "drafts":
        for d in services.outbox.drafts():
            title = f"{d.draft_id} {d.message.subject} -> {d.message.recipient_role} ({d.message.channel.value}, draft)"
            console.print(Panel(d.message.body, title=title, title_align="left"))
    elif name == "audit" and current:
        for e in services.audit_log.entries(current):
            console.print(Text(f"{e.at:%H:%M:%S} {e.kind.value:11} {e.name}", style="dim"))
    else:
        console.print(f"Unknown command {line!r}; /help lists them.")
    return current


if __name__ == "__main__":
    app()
