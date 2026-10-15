"""DocumentIngest stub: serves pre-transcribed documents from fixtures/inbox.

Stands in for fax OCR, an email gateway and call transcription. A real adapter would
receive images, PDFs, MIME messages or audio and return the same `InboundDocument`,
with OCR or transcription confidence attached. A document is visible once the clock
has passed its `received_at`, so a late fax reply appears when the clock moves.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from or_booking.adapters.fixture_data import parse_list
from or_booking.domain.errors import NotFound
from or_booking.domain.models import Channel, Model
from or_booking.ports.clock import Clock
from or_booking.ports.document_ingest import InboundDocument


class _IndexEntry(Model):
    document_id: str
    file: str
    channel: Channel
    received_at: datetime
    sender: str | None = None
    subject: str | None = None


class FixtureDocumentIngest:
    def __init__(self, inbox_dir: Path, clock: Clock) -> None:
        self._dir = inbox_dir
        self._clock = clock
        self._index = {e.document_id: e for e in parse_list(inbox_dir / "index.yaml", _IndexEntry)}

    def list_documents(self) -> list[InboundDocument]:
        now = self._clock.now()
        return [self._read(e) for e in sorted(self._index.values(), key=lambda e: e.received_at) if e.received_at <= now]

    def get_document(self, document_id: str) -> InboundDocument:
        entry = self._index.get(document_id)
        if entry is None or entry.received_at > self._clock.now():
            raise NotFound("document", document_id)
        return self._read(entry)

    def _read(self, e: _IndexEntry) -> InboundDocument:
        return InboundDocument(
            document_id=e.document_id,
            channel=e.channel,
            received_at=e.received_at,
            sender=e.sender,
            subject=e.subject,
            text=(self._dir / e.file).read_text(encoding="utf-8"),
        )
