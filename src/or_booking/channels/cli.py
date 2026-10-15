"""Command-line channel. Builds the services through the composition root and renders with Rich.

Commands grow with the build: `ports` (Phase 0) shows how each port is wired.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from or_booking.app import PORTS, Services, build

app = typer.Typer(no_args_is_help=True, add_completion=False, help="AI-assisted OR case booking (prototype).")
console = Console()


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


if __name__ == "__main__":
    app()
