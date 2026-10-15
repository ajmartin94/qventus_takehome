"""Case sizing: typical (P50) and long (P80) in-room minutes from history (Section 5.5).

The agent sends case length only; the scheduling service adds each room's turnover.
Sizing falls back in steps and says so, so the card can tell the coordinator how much
to trust the number:

1. the surgeon's own history for the procedure, with at least `min_samples` cases
2. the procedure's history across all surgeons, with at least `min_samples` cases
3. the procedure master's default length, with no spread known

A coordinator override is kept beside the original estimate, never in place of it.
"""

from __future__ import annotations

import math
from enum import StrEnum

from or_booking.domain.models import CaseMinutes, Model


class SizingSource(StrEnum):
    SURGEON_HISTORY = "surgeon_history"
    PROCEDURE_HISTORY = "procedure_history"
    PROCEDURE_DEFAULT = "procedure_default"
    OVERRIDE = "override"


class CaseSizing(Model):
    minutes: CaseMinutes
    source: SizingSource
    sample_size: int
    note: str
    estimate: CaseMinutes | None = None  # the agent's estimate, when the coordinator overrode it


def percentile(values: list[int], p: float) -> int:
    """Linear interpolation between closest ranks (the 'inclusive' method), rounded to a minute."""
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    low, high = math.floor(position), math.ceil(position)
    value = ordered[low] + (ordered[high] - ordered[low]) * (position - low)
    return math.floor(value + 0.5)


def size_case(
    surgeon_durations: list[int],
    procedure_durations: list[int],
    default_minutes: int,
    min_samples: int = 5,
) -> CaseSizing:
    if len(surgeon_durations) >= min_samples:
        samples, source = surgeon_durations, SizingSource.SURGEON_HISTORY
        note = f"From the surgeon's last {len(samples)} cases"
    elif len(procedure_durations) >= min_samples:
        samples, source = procedure_durations, SizingSource.PROCEDURE_HISTORY
        note = (
            f"Surgeon has {len(surgeon_durations)} prior cases (fewer than {min_samples}); "
            f"sized from {len(samples)} cases across all surgeons"
        )
    else:
        return CaseSizing(
            minutes=CaseMinutes(typical=default_minutes, long=default_minutes),
            source=SizingSource.PROCEDURE_DEFAULT,
            sample_size=len(procedure_durations),
            note=f"Too little history ({len(procedure_durations)} cases); procedure default length, no spread known. Check with the office",
        )
    return CaseSizing(
        minutes=CaseMinutes(typical=percentile(samples, 0.5), long=percentile(samples, 0.8)),
        source=source,
        sample_size=len(samples),
        note=note,
    )


def override(sizing: CaseSizing, minutes: CaseMinutes) -> CaseSizing:
    """A coordinator's duration override, kept next to the original estimate."""
    return CaseSizing(
        minutes=minutes,
        source=SizingSource.OVERRIDE,
        sample_size=sizing.sample_size,
        note=f"Coordinator override; estimate was {sizing.minutes.typical}/{sizing.minutes.long} min ({sizing.note})",
        estimate=sizing.estimate or sizing.minutes,
    )
