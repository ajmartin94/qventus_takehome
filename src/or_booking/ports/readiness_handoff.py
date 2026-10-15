"""ReadinessHandoff port: hands a booking's readiness list to downstream follow-up.

Stands in for a readiness worklist or Qventus Perioperative Care Coordination. Chasing
the items is downstream of booking (Tier 4).
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from or_booking.domain.models import Model, ReadinessItem


class HandoffReceipt(Model):
    handoff_id: str
    case_id: str
    destination: str
    created_at: datetime
    items: list[ReadinessItem]


@runtime_checkable
class ReadinessHandoff(Protocol):
    def hand_off(self, case_id: str, items: list[ReadinessItem]) -> HandoffReceipt: ...

    def handoffs(self, case_id: str | None = None) -> list[HandoffReceipt]: ...
