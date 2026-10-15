"""Standard booking: one case in one room. The only strategy built in the prototype."""

from __future__ import annotations

from typing import ClassVar

from or_booking.domain.models import AvailabilityQuery, CaseMinutes, SearchPreferences
from or_booking.domain.strategies.base import StrategyKind
from or_booking.domain.validation import QueryInputs


class StandardStrategy:
    kind: ClassVar[StrategyKind] = StrategyKind.STANDARD

    def plan(self, inputs: QueryInputs, minutes: CaseMinutes, preferences: SearchPreferences | None = None) -> AvailabilityQuery:
        """The four facts that find time: surgeon, procedure, case length and date window."""
        return AvailabilityQuery(
            surgeon_id=inputs.surgeon_id,
            procedure_id=inputs.procedure_id,
            case_minutes=minutes,
            window=inputs.window,
            preferences=preferences or SearchPreferences(),
        )
