"""What the orchestrator works with: the ports it needs, the steps a handler returns, and a turn's output."""

from __future__ import annotations

from dataclasses import dataclass, field

from or_booking.domain.models import Model
from or_booking.orchestrator.cards import Card, Reply
from or_booking.orchestrator.states import State
from or_booking.ports import (
    AuditLog,
    Clock,
    Directory,
    DocumentIngest,
    DurationHistory,
    EventSource,
    InboundDocument,
    Outbox,
    PolicyStore,
    ReadinessHandoff,
    SchedulingService,
    Store,
)


@dataclass(frozen=True)
class Ports:
    """Every port the orchestrator uses. The composition root fills it; nothing here knows an adapter."""

    clock: Clock
    audit_log: AuditLog
    store: Store
    scheduling: SchedulingService
    directory: Directory
    duration_history: DurationHistory
    policy_store: PolicyStore
    document_ingest: DocumentIngest
    event_source: EventSource
    outbox: Outbox
    readiness_handoff: ReadinessHandoff


# What a handler returns: move along an edge, rest here (waiting or finished), or hand the
# input to the open request it continues.


@dataclass(frozen=True)
class Go:
    target: State


@dataclass(frozen=True)
class Stay:
    pass


@dataclass(frozen=True)
class Merge:
    request_id: str


STAY = Stay()
Step = Go | Stay | Merge


@dataclass
class TurnOutput:
    incoming: InboundDocument | str | None = None
    lines: list[str] = field(default_factory=list)
    cards: list[Card] = field(default_factory=list)
    trace: list[State] = field(default_factory=list)

    def say(self, text: str) -> None:
        if text:
            self.lines.append(text)

    def card(self, card: Card) -> None:
        self.cards.append(card)

    def reply(self) -> Reply:
        return Reply(message="\n".join(self.lines), cards=self.cards)


class TurnResult(Model):
    request_id: str
    state: State
    trace: list[State]  # states entered during this turn
    reply: Reply
    waiting: bool
