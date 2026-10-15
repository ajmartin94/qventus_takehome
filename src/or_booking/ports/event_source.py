"""EventSource port: hospital and system events that create work on their own.

Stands in for an HL7 SIU scheduling feed (S12 new, S13 reschedule, S14 modify,
S15 cancel) or EHR webhooks. One event can displace several cases.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable

from or_booking.domain.models import Model


class EventType(StrEnum):
    CASE_DISPLACED = "case_displaced"  # bumped for an emergency
    ROOM_CLOSED = "room_closed"  # room, robot or staffing down
    SURGEON_OUT = "surgeon_out"
    TIME_OPENED = "time_opened"  # a release or cancellation freed time


class ScheduleEvent(Model):
    event_id: str
    type: EventType
    occurred_at: datetime
    case_ids: list[str] = []
    room_id: str | None = None
    hl7_message_type: str | None = None  # e.g. "SIU^S15" when the feed is HL7
    detail: str = ""


@runtime_checkable
class EventSource(Protocol):
    def poll(self) -> list[ScheduleEvent]:
        """Events not yet delivered, oldest first."""
        ...
