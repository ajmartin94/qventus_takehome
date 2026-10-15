"""Emergencies take held capacity or displace electives (trauma, transplant, emergent C-section): stub.

Reached only at a hospital whose routing policy lets the agent continue with urgent
requests; Northwind's sends them to the anesthesiologist in charge first. A real
implementation would look for held add-on capacity, then list the elective cases that
could be displaced, and hand the choice to whoever the hospital's policy names.
"""

from __future__ import annotations

from typing import ClassVar

from or_booking.domain.models import CaseMinutes, SearchPreferences, Unsupported
from or_booking.domain.strategies.base import StrategyKind
from or_booking.domain.validation import QueryInputs


class ReserveAndPreemptStrategy:
    kind: ClassVar[StrategyKind] = StrategyKind.RESERVE_AND_PREEMPT

    def plan(self, inputs: QueryInputs, minutes: CaseMinutes, preferences: SearchPreferences | None = None) -> Unsupported:
        return Unsupported(
            capability="Urgent booking into held capacity or by displacing electives",
            reason="Urgent and emergent cases need held add-on capacity or a displacement decision; not supported in the prototype",
            would_need=["held add-on capacity", "the cases that could be displaced", "a decision by whoever policy names"],
        )
