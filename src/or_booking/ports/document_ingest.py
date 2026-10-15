"""DocumentIngest port: turns a fax, email or call into text.

Stands in for fax OCR, an email gateway and call transcription. The prototype adapter
serves pre-transcribed fixture text.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable

from or_booking.domain.models import Channel, Model


class InboundDocument(Model):
    document_id: str
    channel: Channel
    received_at: datetime
    sender: str | None = None
    subject: str | None = None
    text: str


@runtime_checkable
class DocumentIngest(Protocol):
    def list_documents(self) -> list[InboundDocument]: ...

    def get_document(self, document_id: str) -> InboundDocument: ...
