"""Port-call recording (flow guarantee 3: every transition and port call is recorded).

The composition root wraps each integration adapter in `AuditedPort`, so every call
through a port lands in the audit log with its arguments, outcome and the request it
belongs to, without any adapter or handler having to remember to log. The orchestrator
sets the current request with `request_context`.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import date, datetime
from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseModel

from or_booking.domain.errors import BookingError
from or_booking.ports.audit_log import AuditEntry, AuditKind, AuditLog
from or_booking.ports.clock import Clock

current_request_id: ContextVar[str | None] = ContextVar("current_request_id", default=None)

P = TypeVar("P")


@contextmanager
def request_context(request_id: str) -> Iterator[None]:
    token = current_request_id.set(request_id)
    try:
        yield
    finally:
        current_request_id.reset(token)


def summarize(value: Any) -> Any:
    """A compact, JSON-safe rendering of a port argument or result for the audit log."""
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, (list, tuple)):
        return {"count": len(value)}
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return type(value).__name__


class AuditedPort:
    """Transparent proxy: forwards every call to the adapter and records it as a port call."""

    def __init__(self, port_name: str, adapter: Any, audit_log: AuditLog, clock: Clock) -> None:
        self._port_name = port_name
        self._adapter = adapter
        self._audit_log = audit_log
        self._clock = clock

    @property
    def wrapped(self) -> Any:
        return self._adapter

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._adapter, name)
        if name.startswith("_") or not callable(attr):
            return attr
        return self._record(name, attr)

    def _record(self, method: str, fn: Callable[..., Any]) -> Callable[..., Any]:
        def call(*args: Any, **kwargs: Any) -> Any:
            detail: dict[str, Any] = {
                "args": [summarize(a) for a in args],
                "kwargs": {k: summarize(v) for k, v in kwargs.items()},
            }
            try:
                result = fn(*args, **kwargs)
            except BookingError as err:
                detail["error"] = err.to_dict()
                self._write(method, detail)
                raise
            detail["result"] = summarize(result)
            self._write(method, detail)
            return result

        return call

    def _write(self, method: str, detail: dict[str, Any]) -> None:
        self._audit_log.record(
            AuditEntry(
                at=self._clock.now(),
                request_id=current_request_id.get(),
                kind=AuditKind.PORT_CALL,
                name=f"{self._port_name}.{method}",
                detail=detail,
            )
        )


def audited(port_name: str, adapter: P, audit_log: AuditLog, clock: Clock) -> P:
    """Wrap `adapter` so its calls are recorded; typed as the adapter for the caller's sake."""
    return AuditedPort(port_name, adapter, audit_log, clock)  # type: ignore[return-value]
