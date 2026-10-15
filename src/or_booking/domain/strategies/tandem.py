"""Paired rooms run in parallel (cataract lists, flip rooms): stub.

A real implementation would search for two adjacent rooms over the same window, size
the list by case count rather than one case's length, and place the case into an
existing list when one is running. Lists are usually built by the coordinator with the
service line.
"""

from __future__ import annotations

from typing import ClassVar

from or_booking.domain.models import CaseMinutes, SearchPreferences, Unsupported
from or_booking.domain.strategies.base import StrategyKind
from or_booking.domain.validation import QueryInputs


class TandemStrategy:
    kind: ClassVar[StrategyKind] = StrategyKind.TANDEM

    def plan(self, inputs: QueryInputs, minutes: CaseMinutes, preferences: SearchPreferences | None = None) -> Unsupported:
        return Unsupported(
            capability="Paired-room (tandem) booking",
            reason=f"{inputs.procedure_id} runs as a list in paired rooms; building or joining a list isn't supported in the prototype",
            would_need=["two rooms over the same window", "a list sized by case count"],
        )
