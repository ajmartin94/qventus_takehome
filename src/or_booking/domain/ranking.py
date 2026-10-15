"""Ranking options and the facts on each card (Section 5.6).

The scheduling service decides what is bookable; the agent decides how to present it.
The order is presentation, not enforcement: the coordinator chooses.

1. the requesting surgeon's own block, if the case fits at its typical length
2. options that fit at the long length, earliest first
3. options that fit only at the typical length, earliest first
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from typing import Literal

from or_booking.domain.models import (
    AvailabilityResult,
    CaseMinutes,
    Model,
    OptionGroup,
    Ownership,
    RankedOption,
    SlotOption,
)

_GROUP_ORDER = {OptionGroup.OWN_BLOCK: 0, OptionGroup.FITS_LONG: 1, OptionGroup.FITS_TYPICAL_ONLY: 2}


def rank_options(
    options: list[SlotOption],
    minutes: CaseMinutes,
    today: date,
    readiness_risks: Mapping[str, list[str]] | None = None,
    limit: int = 3,
) -> list[RankedOption]:
    """`readiness_risks` maps option ids to the risks computed for that date (readiness.readiness_risks)."""
    risks = readiness_risks or {}
    candidates = []
    for option in options:
        capacity = option.case_capacity_minutes
        if not option.bookable or capacity < minutes.typical:
            continue
        own = option.ownership is Ownership.OWN_BLOCK
        fits_long = capacity >= minutes.long
        group = OptionGroup.OWN_BLOCK if own else OptionGroup.FITS_LONG if fits_long else OptionGroup.FITS_TYPICAL_ONLY
        candidates.append((option, group, fits_long, max(0, minutes.long - capacity)))

    candidates.sort(key=lambda c: (_GROUP_ORDER[c[1]], c[0].start, c[0].room_id))
    return [
        RankedOption(
            rank=rank,
            option=option,
            group=group,
            fits_typical=True,
            fits_long=fits_long,
            overrun_minutes=overrun,
            counts_toward_block=option.ownership is Ownership.OWN_BLOCK,
            days_until_surgery=(option.date - today).days,
            readiness_risks=risks.get(option.option_id, []),
        )
        for rank, (option, group, fits_long, overrun) in enumerate(candidates[:limit], start=1)
    ]


class DayStatus(Model):
    """Why a day the coordinator asked for is or isn't offered: the separate line under the cards."""

    day: date
    status: Literal["bookable", "held_by_other", "schedule_closed", "no_fit"]
    held: list[SlotOption] = []  # windows in other owners' blocks that would fit, with release times


def requested_day_status(day: date, result: AvailabilityResult) -> DayStatus:
    if any(o.date == day for o in result.options):
        return DayStatus(day=day, status="bookable")
    if day in result.closed_dates:
        return DayStatus(day=day, status="schedule_closed")
    held = [o for o in result.held if o.date == day]
    return DayStatus(day=day, status="held_by_other", held=held) if held else DayStatus(day=day, status="no_fit")
