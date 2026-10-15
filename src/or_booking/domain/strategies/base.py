"""The BookingStrategy seam: how a case is booked, chosen from the procedure's attributes."""

from __future__ import annotations

from enum import StrEnum
from typing import ClassVar, Protocol

from or_booking.domain.models import AvailabilityQuery, CaseMinutes, SearchPreferences, Unsupported
from or_booking.domain.validation import QueryInputs


class StrategyKind(StrEnum):
    STANDARD = "standard"  # one room, one case
    BED_COUPLED = "bed_coupled"  # OR plus an ICU bed, booked together
    TANDEM = "tandem"  # paired rooms run in parallel by one surgeon
    RESERVE_AND_PREEMPT = "reserve_and_preempt"  # emergencies take held capacity or displace electives


class BookingStrategy(Protocol):
    kind: ClassVar[StrategyKind]

    def plan(
        self, inputs: QueryInputs, minutes: CaseMinutes, preferences: SearchPreferences | None = None
    ) -> AvailabilityQuery | Unsupported:
        """The availability query this strategy sends, or why it can't be booked here yet."""
        ...
