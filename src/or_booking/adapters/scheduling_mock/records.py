"""The scheduling system's own records, as fixtures/scheduling holds them.

These shapes are internal to the mock: they describe how the simulated scheduling
system stores its suite settings, rooms, equipment, block templates and cases. The
agent never sees them; it sees only what the `SchedulingService` port returns.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Literal

from or_booking.adapters.fixture_data import parse, parse_list, read_yaml
from or_booking.domain.models import AnesthesiaType, ImplantRequest, Laterality, Model, PatientClass

Weekday = Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
WEEKDAYS: tuple[Weekday, ...] = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


class TimeRange(Model):
    start: time
    end: time


class ScheduleClose(Model):
    business_days_before: int
    at: time


class LocationRecord(Model):
    id: str
    name: str
    timezone: str
    operating_days: list[Weekday]
    prime_time: TimeRange
    schedule_close: ScheduleClose
    hold_minutes: int


class RoomRecord(Model):
    id: str
    type: str
    capabilities: list[str]
    turnover_minutes: int


class AssetRecord(Model):
    id: str
    type: str
    name: str
    rooms: list[str]


class ReleaseHorizon(Model):
    days_before: int
    at: time


class BlockTemplate(Model):
    """A weekly allocation of a room's time to an owner, with its own release horizon."""

    id: str
    owner: str  # a surgeon id or a group id
    room: str
    weekday: Weekday
    start: time
    end: time
    release: ReleaseHorizon
    filler: bool = False


class EarlyRelease(Model):
    block: str
    date: date
    start: time
    end: time
    released_at: datetime
    reason: str = ""


class BlocksFile(Model):
    release_horizons: dict[str, ReleaseHorizon] = {}
    groups: dict[str, str]
    blocks: list[BlockTemplate]
    early_releases: list[EarlyRelease] = []


class FixtureCase(Model):
    case_id: str
    surgeon_id: str
    procedure_id: str
    room_id: str
    date: date
    start: time
    end: time
    laterality: Laterality | None = None
    patient_mrn: str | None = None
    diagnosis_code: str | None = None
    anesthesia_type: AnesthesiaType | None = None
    patient_class: PatientClass | None = None
    implants: list[ImplantRequest] = []
    assets: list[str] = []


class BookedCasesFile(Model):
    schedule_filled_through: date | None = None
    cases: list[FixtureCase]


@dataclass(frozen=True)
class SchedulingRecords:
    location: LocationRecord
    rooms: dict[str, RoomRecord]
    assets: dict[str, AssetRecord]
    blocks: BlocksFile
    booked: BookedCasesFile


def load_scheduling(fixtures_dir: Path) -> SchedulingRecords:
    folder = fixtures_dir / "scheduling"
    return SchedulingRecords(
        location=parse(folder / "location.yaml", read_yaml(folder / "location.yaml"), LocationRecord),
        rooms={r.id: r for r in parse_list(folder / "rooms.yaml", RoomRecord)},
        assets={a.id: a for a in parse_list(folder / "assets.yaml", AssetRecord)},
        blocks=parse(folder / "blocks.yaml", read_yaml(folder / "blocks.yaml"), BlocksFile),
        booked=parse(folder / "booked_cases.yaml", read_yaml(folder / "booked_cases.yaml"), BookedCasesFile),
    )
