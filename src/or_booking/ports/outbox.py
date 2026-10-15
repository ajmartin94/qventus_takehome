"""Outbox port: notifications to the office, patient, SPD, vendor or a block owner.

In the prototype every message is a draft for a person to approve; nothing is sent.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Protocol, runtime_checkable

from or_booking.domain.models import Channel, Contact, Model


class OutboundMessage(Model):
    request_id: str
    recipient_role: str  # e.g. surgeons_office, patient, spd, vendor, block_owner
    recipient: Contact | None = None
    channel: Channel
    subject: str
    body: str


class DraftRecord(Model):
    draft_id: str
    created_at: datetime
    status: Literal["draft"] = "draft"
    message: OutboundMessage


@runtime_checkable
class Outbox(Protocol):
    def draft(self, message: OutboundMessage) -> DraftRecord: ...

    def drafts(self, request_id: str | None = None) -> list[DraftRecord]: ...
