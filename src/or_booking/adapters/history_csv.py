"""DurationHistory adapter over a CSV of past cases (fixtures/ehr/case_history.csv).

Stands in for EHR case logs or an analytics warehouse.
"""

from __future__ import annotations

import csv
from pathlib import Path


class CsvDurationHistory:
    def __init__(self, path: Path) -> None:
        with path.open(newline="", encoding="utf-8") as f:
            self._rows = [(r["surgeon_id"], r["procedure_id"], int(r["in_room_minutes"])) for r in csv.DictReader(f)]

    def surgeon_durations(self, surgeon_id: str, procedure_id: str) -> list[int]:
        return [m for s, p, m in self._rows if s == surgeon_id and p == procedure_id]

    def procedure_durations(self, procedure_id: str) -> list[int]:
        return [m for _, p, m in self._rows if p == procedure_id]
