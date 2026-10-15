"""Command-line channel. Builds the services through the composition root and renders with Rich.

Commands grow with the build:
- `ports` (Phase 0): how each port is wired.
- `availability` and `schedule` (Phase 1): raw views of the scheduling service, for
  checking the simulated hospital. The agent's own option cards come in Phase 3.
"""

from __future__ import annotations

from datetime import date

import typer
from rich.console import Console
from rich.table import Table

from or_booking.app import PORTS, Services, build
from or_booking.domain.errors import BookingError
from or_booking.domain.models import AvailabilityQuery, CaseMinutes, DateWindow, SlotOption

app = typer.Typer(no_args_is_help=True, add_completion=False, help="AI-assisted OR case booking (prototype).")
console = Console()

_STATE_STYLE = {"held": "blue", "released": "green", "open": "white"}


def _services() -> Services:
    return build()


@app.callback()
def main() -> None:
    """AI-assisted OR case booking (prototype)."""


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
    services = _services()
    view = services.scheduling.get_schedule(DateWindow(start=date.fromisoformat(start), end=date.fromisoformat(end)))
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
            for s in rd.segments:
                owner = s.owner_name or "open time"
                if s.filler:
                    lines.append(f"[dim]{owner} (booked)[/dim]")
                else:
                    lines.append(f"[{_STATE_STYLE[s.state]}]{s.start:%H:%M} {owner}[/{_STATE_STYLE[s.state]}]")
            lines += [f"  {c.start:%H:%M}-{c.end:%H:%M} {c.procedure_id}" for c in rd.cases]
            cells.append("\n".join(lines))
        table.add_row(room, *cells)
    console.print(table)


if __name__ == "__main__":
    app()
