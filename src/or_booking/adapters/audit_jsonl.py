"""AuditLog adapters: a JSON-lines file, and an in-memory log for tests.

Production would ship the same entries to a SIEM or an OpenTelemetry pipeline.
"""

from __future__ import annotations

from pathlib import Path

from or_booking.ports.audit_log import AuditEntry


class MemoryAuditLog:
    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self._entries.append(entry)

    def entries(self, request_id: str | None = None) -> list[AuditEntry]:
        return [e for e in self._entries if request_id is None or e.request_id == request_id]


class JsonlAuditLog:
    """Appends one JSON object per line. The file is the durable record; reads parse it back."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, entry: AuditEntry) -> None:
        with self._path.open("a", encoding="utf-8") as f:
            f.write(entry.model_dump_json() + "\n")

    def entries(self, request_id: str | None = None) -> list[AuditEntry]:
        if not self._path.exists():
            return []
        with self._path.open(encoding="utf-8") as f:
            parsed = [AuditEntry.model_validate_json(line) for line in f if line.strip()]
        return [e for e in parsed if request_id is None or e.request_id == request_id]
