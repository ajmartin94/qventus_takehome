"""SchedulingService port: the OR scheduling system of record.

The service owns its own rules (block release, schedule close, room capability,
turnover, shared equipment, privileges, holds) and reports their effect: options with
their ownership state, or a typed error. The agent never re-implements them.

Errors each method may raise (all from `or_booking.domain.errors`):

- search_availability: NotPrivileged, NotFound
- place_hold: SlotTaken, BlockNotReleased, PastCutoff, ResourceConflict, NotFound
- confirm_booking: HoldExpired, PastCutoff, NotPrivileged, MissingRequiredField,
  ResourceConflict, RequestRejected, NotFound. A repeated idempotency key returns the
  case already created, never a second one.
- cancel_case, get_case: NotFound; reschedule_case: the hold errors above, NotFound
- update_case: MissingRequiredField, NotFound. Idempotent on the update's key.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Protocol, runtime_checkable

from or_booking.domain.models import (
    AvailabilityQuery,
    AvailabilityResult,
    BookedCase,
    BookingRequest,
    CaseStatus,
    CaseUpdate,
    DateWindow,
    Hold,
    Model,
)


class ScheduleSegment(Model):
    """A stretch of a room's prime time and who owns it, from no particular surgeon's view."""

    start: datetime
    end: datetime
    state: Literal["held", "released", "open"]
    owner_id: str | None = None
    owner_name: str | None = None
    releases_at: datetime | None = None
    released_at: datetime | None = None
    filler: bool = False  # simulated as fully booked by cases the fixture doesn't list


class ScheduledCase(Model):
    case_id: str
    status: CaseStatus
    surgeon_id: str
    procedure_id: str
    patient_mrn: str | None = None
    start: datetime
    end: datetime


class RoomDay(Model):
    room_id: str
    date: date
    schedule_closed: bool
    fully_booked: bool  # the whole day is simulated as booked
    segments: list[ScheduleSegment]
    cases: list[ScheduledCase]


class ScheduleView(Model):
    window: DateWindow
    room_days: list[RoomDay]


@runtime_checkable
class SchedulingService(Protocol):
    def search_availability(self, query: AvailabilityQuery) -> AvailabilityResult:
        """Bookable options (own block, released, open) plus windows held by other owners, with release times."""
        ...

    def place_hold(self, option_id: str, request_id: str) -> Hold:
        """Protect an offered option for the service's hold time limit. One active hold per request."""
        ...

    def release_hold(self, hold_id: str) -> None: ...

    def confirm_booking(self, hold_id: str, request: BookingRequest) -> BookedCase:
        """Commit the booking against a live hold. Idempotent on `request.idempotency_key`."""
        ...

    def get_case(self, case_id: str) -> BookedCase: ...

    def find_cases(self, *, patient_mrn: str | None = None, surgeon_id: str | None = None) -> list[BookedCase]: ...

    def cancel_case(self, case_id: str, reason: str) -> BookedCase: ...

    def reschedule_case(self, case_id: str, hold_id: str, idempotency_key: str) -> BookedCase: ...

    def update_case(self, update: CaseUpdate) -> BookedCase:
        """Change a booked case's details without moving it."""
        ...

    def get_schedule(self, window: DateWindow) -> ScheduleView:
        """Read-only view of blocks and cases per room per day, for the schedule grid."""
        ...
