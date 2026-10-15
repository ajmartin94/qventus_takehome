"""OR plus ICU bed (cardiac, transplant): stub.

A real implementation would query OR availability and the ICU bed forecast for the
post-op nights together, hold both, and commit them as one unit, releasing the room
hold if the bed can't be secured. In most hospitals that bed comes from bed management,
so the strategy needs a bed-management port the prototype doesn't have.
"""

from __future__ import annotations

from typing import ClassVar

from or_booking.domain.models import CaseMinutes, SearchPreferences, Unsupported
from or_booking.domain.strategies.base import StrategyKind
from or_booking.domain.validation import QueryInputs


class BedCoupledStrategy:
    kind: ClassVar[StrategyKind] = StrategyKind.BED_COUPLED

    def plan(self, inputs: QueryInputs, minutes: CaseMinutes, preferences: SearchPreferences | None = None) -> Unsupported:
        return Unsupported(
            capability="OR plus ICU bed booking",
            reason=f"{inputs.procedure_id} goes to the ICU after surgery; booking the room and the bed together isn't supported in the prototype",
            would_need=["OR time", "ICU bed for the post-op nights", "bed management confirmation"],
        )
