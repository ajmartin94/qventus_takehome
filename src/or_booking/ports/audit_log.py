"""AuditLog port: every transition, model call and port call is recorded (flow guarantee 3)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

from or_booking.domain.models import Model


class AuditKind(StrEnum):
    TRANSITION = "transition"
    MODEL_CALL = "model_call"
    PORT_CALL = "port_call"
    DECISION = "decision"


class AuditEntry(Model):
    at: datetime
    request_id: str | None = None
    kind: AuditKind
    name: str  # e.g. "scheduling.place_hold" or "Presenting -> Holding"
    detail: dict[str, Any] = {}


@runtime_checkable
class AuditLog(Protocol):
    def record(self, entry: AuditEntry) -> None: ...

    def entries(self, request_id: str | None = None) -> list[AuditEntry]: ...
