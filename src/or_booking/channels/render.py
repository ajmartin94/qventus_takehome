"""Rich rendering of replies and cards for the CLI. Cards are data from the orchestrator; this only draws them."""

from __future__ import annotations

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from or_booking.domain.models import ReadinessItem
from or_booking.orchestrator.cards import AnswerCard, Card, ConfirmationCard, HandoffCard, OptionsCard, OutcomeCard
from or_booking.orchestrator.context import TurnResult

_STATUS_STYLE = {"done": "green", "open": "white", "at_risk": "yellow", "overdue": "red"}


def trace_line(result: TurnResult) -> Text:
    states = " -> ".join(s.value for s in result.trace) or f"(stays in {result.state.value})"
    suffix = "  waiting" if result.waiting else ""
    return Text(f"{result.request_id}: {states}{suffix}", style="dim")


def render_result(result: TurnResult) -> RenderableType:
    parts: list[RenderableType] = [trace_line(result)]
    if result.reply.message:
        parts.append(Text(result.reply.message, style="bold"))
    parts += [render_card(c) for c in result.reply.cards]
    return Group(*parts)


def render_card(card: Card) -> RenderableType:
    if isinstance(card, OptionsCard):
        return _options(card)
    if isinstance(card, ConfirmationCard):
        return _confirmation(card)
    if isinstance(card, OutcomeCard):
        return _outcome(card)
    if isinstance(card, HandoffCard):
        return _handoff(card)
    if isinstance(card, AnswerCard):
        return _answer(card)
    raise TypeError(f"unknown card {card!r}")


def _options(card: OptionsCard) -> RenderableType:
    table = Table(title=card.title, title_justify="left", caption=card.sizing, caption_justify="left")
    for column in ("#", "Day", "Room", "Window", "Ownership", "Fit", "Days out", "Readiness risk"):
        table.add_column(column)
    for o in card.options:
        ownership = o.ownership + (" (counts toward block)" if o.counts_toward_block else "")
        table.add_row(str(o.number), o.day, o.room, o.window, ownership, o.fit, str(o.days_until_surgery), "; ".join(o.readiness_risks) or "none")
    parts: list[RenderableType] = [table]
    if card.still_needed:
        parts.append(Text("Still needed to book: " + "; ".join(card.still_needed), style="yellow"))
    return Group(*parts)


def _confirmation(card: ConfirmationCard) -> RenderableType:
    table = Table(title_justify="left", show_header=True, box=None)
    for column in ("Field", "Value", "Source"):
        table.add_column(column)
    for row in card.rows:
        table.add_row(row.field, row.value, Text(row.source, style="dim"))
    footer = [f"Hold expires {card.hold_expires}" if card.hold_expires else "", card.straight_through]
    return Panel(
        Group(Text(card.slot, style="bold"), table, Text("  ".join(x for x in footer if x), style="dim")),
        title=card.title,
        title_align="left",
        border_style="cyan",
    )


def _readiness(items: list[ReadinessItem]) -> Table:
    table = Table(title="Readiness list (handed off)", title_justify="left")
    for column in ("Item", "Owner", "Due", "Status", "Note"):
        table.add_column(column)
    for i in items:
        due = f"{i.due:%a %b %d %H:%M}" if i.due else (f"dated {i.valid_from:%b %d} or later" if i.valid_from else "-")
        table.add_row(i.item, i.owner, due, Text(i.status.value, style=_STATUS_STYLE[i.status.value]), i.detail)
    return table


def _rows(rows: list[tuple[str, str]]) -> Table:
    table = Table(show_header=False, box=None)
    table.add_column(style="bold")
    table.add_column()
    for key, value in rows:
        table.add_row(key, value)
    return table


def _outcome(card: OutcomeCard) -> RenderableType:
    parts: list[RenderableType] = [_rows(card.rows)]
    if card.readiness:
        parts.append(_readiness(card.readiness))
    parts += [Text(f"Draft: {d}", style="dim") for d in card.drafts]
    return Panel(Group(*parts), title=card.title, title_align="left", border_style="green")


def _handoff(card: HandoffCard) -> RenderableType:
    rows = [("Reason", card.reason), ("Action", card.action), ("Policy", card.policy), *card.fields]
    return Panel(_rows(rows), title=card.title, title_align="left", border_style="dark_orange")


def _answer(card: AnswerCard) -> RenderableType:
    parts: list[RenderableType] = [_rows(card.rows)]
    if card.readiness:
        parts.append(_readiness(card.readiness))
    return Panel(Group(*parts), title=card.title, title_align="left")
