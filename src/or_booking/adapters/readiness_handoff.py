"""ReadinessHandoff stub: records the readiness list a booking hands downstream.

Stands in for a readiness worklist or Qventus Perioperative Care Coordination, where
each item would become a tracked task with its owner and due date. Chasing the items
is downstream of booking.
"""

from __future__ import annotations

from or_booking.domain.models import ReadinessItem
from or_booking.ports.clock import Clock
from or_booking.ports.readiness_handoff import HandoffReceipt


class RecordedReadinessHandoff:
    def __init__(self, clock: Clock, destination: str = "readiness worklist (recorded only)") -> None:
        self._clock = clock
        self._destination = destination
        self._receipts: list[HandoffReceipt] = []

    def hand_off(self, case_id: str, items: list[ReadinessItem]) -> HandoffReceipt:
        receipt = HandoffReceipt(
            handoff_id=f"RH-{len(self._receipts) + 1:04d}",
            case_id=case_id,
            destination=self._destination,
            created_at=self._clock.now(),
            items=items,
        )
        self._receipts.append(receipt)
        return receipt

    def handoffs(self, case_id: str | None = None) -> list[HandoffReceipt]:
        return [r for r in self._receipts if case_id is None or r.case_id == case_id]
