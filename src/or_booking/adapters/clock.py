"""Clock adapters: a frozen clock for demos and tests, and the system clock."""

from __future__ import annotations

from datetime import datetime, timedelta


class FrozenClock:
    """Stays at one moment until moved. Demos run at Wed Oct 14, 2026 09:00."""

    def __init__(self, at: datetime) -> None:
        self._now = at

    def now(self) -> datetime:
        return self._now

    def set(self, at: datetime) -> None:
        self._now = at

    def advance(self, **delta: float) -> datetime:
        """Move forward, e.g. `advance(minutes=11)` to let a hold expire."""
        self._now += timedelta(**delta)
        return self._now


class SystemClock:
    def now(self) -> datetime:
        return datetime.now().replace(microsecond=0)
