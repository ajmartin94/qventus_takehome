"""Outbox stub: records drafts and never sends.

Stands in for fax, email, secure messaging or Qventus outreach. Every message waits
for a person to approve it; a real adapter would deliver approved drafts and record
delivery receipts.
"""

from __future__ import annotations

from or_booking.ports.clock import Clock
from or_booking.ports.outbox import DraftRecord, OutboundMessage


class DraftOutbox:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._drafts: list[DraftRecord] = []

    def draft(self, message: OutboundMessage) -> DraftRecord:
        record = DraftRecord(draft_id=f"D-{len(self._drafts) + 1:04d}", created_at=self._clock.now(), message=message)
        self._drafts.append(record)
        return record

    def drafts(self, request_id: str | None = None) -> list[DraftRecord]:
        return [d for d in self._drafts if request_id is None or d.message.request_id == request_id]
