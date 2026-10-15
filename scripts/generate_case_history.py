"""Generate fixtures/ehr/case_history.csv: ~150 past cases over 18 months, fixed seed.

Most surgeon/procedure pairs are random draws around a plausible mean. Two pairs are
constructed so the demo numbers are exact under any common percentile method:

- Dr. Patel, TKA-ROBOTIC: 14 cases, P50 112 minutes, P80 135 minutes
- Dr. Chen, TKA: 20 cases, P50 98 minutes

The values on either side of each percentile's position are pinned to the target, so
the median, the interpolated P80 and the nearest-rank P80 all agree.

A few pairs have fewer than 5 cases on purpose, so sizing's fallbacks are exercised.

Usage: python scripts/generate_case_history.py
"""

from __future__ import annotations

import csv
import math
import random
import statistics
from datetime import date, timedelta
from pathlib import Path

SEED = 20261014
OUT = Path(__file__).resolve().parents[1] / "fixtures" / "ehr" / "case_history.csv"
START, END = date(2025, 4, 1), date(2026, 9, 30)

# (surgeon, procedure, cases, mean minutes, standard deviation)
RANDOM_PAIRS = [
    ("S-PATEL", "TKA", 6, 101, 12),
    ("S-PATEL", "UKA-ROBOTIC", 3, 88, 10),  # < 5: sizing falls back to all surgeons
    ("S-PATEL", "THA", 12, 96, 11),
    ("S-CHEN", "THA", 10, 106, 13),
    ("S-CHEN", "KNEE-SCOPE", 16, 46, 7),
    ("S-RUIZ", "PROSTATECTOMY-ROBOTIC", 15, 212, 25),
    ("S-OKAFOR", "LAP-CHOLE", 18, 76, 12),
    ("S-OKAFOR", "HERNIA-ROBOTIC", 9, 118, 15),
    ("S-LEE", "CABG", 10, 298, 30),
    ("S-ALVAREZ", "CATARACT", 20, 22, 4),
    ("S-MEHTA", "TIBIA-NAIL", 4, 112, 18),  # < 5 across all surgeons: falls back to the procedure default
]


def pinned(rng: random.Random, n: int, pins: dict[int, int], low: int, high: int) -> list[int]:
    """`n` values whose sorted order has the given (0-based) positions fixed.

    Every other value is drawn between its neighbouring pins, so sorting can't move a pin.
    """
    values = []
    for i in range(n):
        if i in pins:
            values.append(pins[i])
            continue
        below = max((v for j, v in pins.items() if j < i), default=low)
        above = min((v for j, v in pins.items() if j > i), default=high)
        values.append(rng.randint(below, above))
    return sorted(values)


def patel_robotic_tka(rng: random.Random) -> list[int]:
    # n=14: median averages positions 6 and 7; P80 sits at 10.4 (inclusive), 12th value (nearest rank)
    return pinned(rng, 14, {6: 112, 7: 112, 10: 135, 11: 135}, low=94, high=162)


def chen_tka(rng: random.Random) -> list[int]:
    # n=20: median averages positions 9 and 10; P80 between positions 15 and 16
    return pinned(rng, 20, {9: 98, 10: 98, 15: 118, 16: 118}, low=80, high=140)


def weekdays(rng: random.Random, n: int) -> list[date]:
    days = [START + timedelta(d) for d in range((END - START).days + 1)]
    return sorted(rng.sample([d for d in days if d.weekday() < 5], n))


def main() -> None:
    rng = random.Random(SEED)
    rows: list[tuple[str, str, date, int]] = []

    def add(surgeon: str, procedure: str, minutes: list[int]) -> None:
        shuffled = minutes[:]
        rng.shuffle(shuffled)
        rows.extend((surgeon, procedure, d, m) for d, m in zip(weekdays(rng, len(shuffled)), shuffled))

    add("S-PATEL", "TKA-ROBOTIC", patel_robotic_tka(rng))
    add("S-CHEN", "TKA", chen_tka(rng))
    for surgeon, procedure, n, mean, sd in RANDOM_PAIRS:
        add(surgeon, procedure, [max(10, round(rng.gauss(mean, sd))) for _ in range(n)])

    rows.sort(key=lambda r: (r[2], r[0], r[1]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "surgeon_id", "procedure_id", "date", "in_room_minutes"])
        for i, (surgeon, procedure, day, minutes) in enumerate(rows, start=1):
            writer.writerow([f"H-{i:05d}", surgeon, procedure, day.isoformat(), minutes])

    check(rows)
    print(f"wrote {len(rows)} cases to {OUT}")


def check(rows: list[tuple[str, str, date, int]]) -> None:
    def minutes(surgeon: str, procedure: str) -> list[int]:
        return sorted(m for s, p, _, m in rows if (s, p) == (surgeon, procedure))

    patel = minutes("S-PATEL", "TKA-ROBOTIC")
    assert len(patel) == 14 and statistics.median(patel) == 112
    assert statistics.quantiles(patel, n=10, method="inclusive")[7] == 135
    assert statistics.quantiles(patel, n=10, method="exclusive")[7] == 135
    assert patel[math.ceil(0.8 * len(patel)) - 1] == 135
    chen = minutes("S-CHEN", "TKA")
    assert len(chen) == 20 and statistics.median(chen) == 98


if __name__ == "__main__":
    main()
