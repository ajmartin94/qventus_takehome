"""DurationHistory port: historical in-room minutes, from EHR case logs or an analytics warehouse.

Returns raw samples; sizing (P50 / P80 and the fallbacks) is domain logic.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class DurationHistory(Protocol):
    def surgeon_durations(self, surgeon_id: str, procedure_id: str) -> list[int]: ...

    def procedure_durations(self, procedure_id: str) -> list[int]: ...
