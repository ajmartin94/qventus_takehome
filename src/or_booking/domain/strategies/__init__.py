"""Booking strategies (Section 5.8): chosen from the procedure's attributes, never configured per site.

Only `standard` builds an availability query. The stubs return `Unsupported` with a
reason, which the orchestrator treats as the `unsupported_booking_strategy` situation;
the hospital's routing policy says who takes it.
"""

from __future__ import annotations

from or_booking.domain.models import PostOpDestination, Procedure, Surgeon
from or_booking.domain.strategies.base import BookingStrategy, StrategyKind
from or_booking.domain.strategies.bed_coupled import BedCoupledStrategy
from or_booking.domain.strategies.reserve_and_preempt import ReserveAndPreemptStrategy
from or_booking.domain.strategies.standard import StandardStrategy
from or_booking.domain.strategies.tandem import TandemStrategy

STRATEGIES: dict[StrategyKind, BookingStrategy] = {
    s.kind: s for s in (StandardStrategy(), BedCoupledStrategy(), TandemStrategy(), ReserveAndPreemptStrategy())
}


def select_strategy(procedure: Procedure, surgeon: Surgeon, stated_urgency: str = "none") -> BookingStrategy:
    if stated_urgency in ("urgent", "emergent"):
        kind = StrategyKind.RESERVE_AND_PREEMPT
    elif procedure.post_op is PostOpDestination.ICU:
        kind = StrategyKind.BED_COUPLED
    elif procedure.tandem_eligible and surgeon.runs_paired_rooms:
        kind = StrategyKind.TANDEM
    else:
        kind = StrategyKind.STANDARD
    return STRATEGIES[kind]


__all__ = ["STRATEGIES", "BookingStrategy", "StrategyKind", "select_strategy"]
