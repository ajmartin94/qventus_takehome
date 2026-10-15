"""Clock port. Every component reads time through it, so demos and tests can freeze it.

All times in the system are the hospital's local wall-clock time (naive datetimes).
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class Clock(Protocol):
    def now(self) -> datetime: ...
