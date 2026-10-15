"""Per-request state, persisted through the Store port after every turn (Section 6.7).

One session per request or re-booking task. Any channel can resume it: a fax reply
matched to an open draft continues the same session hours later.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict

from or_booking.domain.models import (
    AvailabilityResult,
    BookingRequest,
    CaseDraft,
    CaseUpdate,
    Contact,
    Hold,
    Issue,
    RankedOption,
    ReadinessItem,
)
from or_booking.domain.policy import Route
from or_booking.domain.sizing import CaseSizing
from or_booking.domain.straight_through import StraightThroughVerdict
from or_booking.interpretation.schemas import Intent
from or_booking.orchestrator.states import TERMINAL, State
from or_booking.ports.event_source import ScheduleEvent
from or_booking.ports.store import Store


class SessionKind(StrEnum):
    NEW = "new"  # a case to book
    RESCHEDULE = "reschedule"  # a booked case that needs a new slot
    UPDATE = "update"  # a booked case that keeps its slot
    CANCEL = "cancel"
    INQUIRY = "inquiry"  # status or availability, answered read-only


class TranscriptEntry(BaseModel):
    at: datetime
    speaker: Literal["coordinator", "requester", "agent"]
    text: str
    channel: str | None = None


class Session(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    kind: SessionKind = SessionKind.NEW
    state: State = State.START
    interactive: bool = True  # a coordinator is in the conversation to answer questions
    coordinator_id: str
    draft: CaseDraft
    intent: Intent | None = None
    requester: Contact | None = None
    source_document: str | None = None
    event: ScheduleEvent | None = None
    case_id: str | None = None  # the booked case this request is about, or produced
    parent_request_id: str | None = None

    sizing: CaseSizing | None = None
    availability: AvailabilityResult | None = None
    ranked: list[RankedOption] = []
    selected_option_id: str | None = None
    hold: Hold | None = None
    booking_request: BookingRequest | None = None
    case_update: CaseUpdate | None = None

    issues: list[Issue] = []
    open_question: Issue | None = None
    last_question: str | None = None
    reader_notes: list[str] = []  # what the model couldn't interpret in the last input, in its words
    attempts: dict[str, int] = {}
    reply_deadline: datetime | None = None
    cancel_reason: str | None = None

    route: Route | None = None
    route_reason: str | None = None
    summary: str | None = None  # the one-line answer, for requests answered read-only
    answer: list[tuple[str, str]] = []
    readiness: list[ReadinessItem] = []
    verdict: StraightThroughVerdict | None = None
    drafts: list[str] = []

    path: list[State] = []  # every state entered, in order
    transcript: list[TranscriptEntry] = []
    created_at: datetime
    updated_at: datetime

    @property
    def finished(self) -> bool:
        return self.state in TERMINAL


class _Counter(BaseModel):
    value: int


class SessionRepository:
    COLLECTION = "sessions"

    def __init__(self, store: Store) -> None:
        self._store = store

    def save(self, session: Session) -> None:
        self._store.save(self.COLLECTION, session.request_id, session)

    def load(self, request_id: str) -> Session | None:
        return self._store.load(self.COLLECTION, request_id, Session)

    def all(self) -> list[Session]:
        return self._store.list(self.COLLECTION, Session)

    def open(self) -> list[Session]:
        return [s for s in self.all() if not s.finished]

    def next_request_id(self) -> str:
        counter = self._store.load("counters", "request", _Counter) or _Counter(value=0)
        counter = _Counter(value=counter.value + 1)
        self._store.save("counters", "request", counter)
        return f"REQ-{counter.value:04d}"
