"""The mock scheduling service against Northwind's data: the D1 story and the rules it enforces."""

from __future__ import annotations

from dataclasses import replace
from datetime import date, datetime

import pytest

from or_booking.adapters.clock import FrozenClock
from or_booking.adapters.fixture_data import FixtureError, load_ehr
from or_booking.adapters.scheduling_mock import MockSchedulingService
from or_booking.adapters.scheduling_mock.records import FixtureCase, load_scheduling
from or_booking.domain.errors import PastCutoff, ResourceConflict
from or_booking.domain.models import AvailabilityQuery, CaseMinutes, DateWindow, Ownership
from tests.conftest import DEMO_NOW, FIXTURES

TARGET_WEEK = DateWindow(start=date(2026, 11, 2), end=date(2026, 11, 6))
D1_QUERY = AvailabilityQuery(
    surgeon_id="S-PATEL",
    procedure_id="TKA-ROBOTIC",
    case_minutes=CaseMinutes(typical=112, long=135),
    window=TARGET_WEEK,
)


def service_at(now: datetime) -> MockSchedulingService:
    return MockSchedulingService.from_fixtures(FIXTURES, FrozenClock(now))


def summary(option) -> tuple:
    return (option.option_id, option.ownership, option.block_owner_id, option.window_minutes)


def test_d1_returns_tuesday_thursday_friday_and_reports_wednesday_held() -> None:
    result = service_at(DEMO_NOW).search_availability(D1_QUERY)

    assert [summary(o) for o in result.options] == [
        ("OPT-OR5-20261103-1300", Ownership.OWN_BLOCK, "S-PATEL", 150),  # Patel's robotic block
        ("OPT-OR6-20261105-0730", Ownership.OPEN, None, 240),  # open time
        ("OPT-OR5-20261106-1200", Ownership.RELEASED, "S-CHEN", 210),  # released early by Dr. Chen
    ]
    assert [(o.option_id, o.block_owner_id, o.releases_at) for o in result.held] == [
        ("OPT-OR5-20261104-1130", "S-CHEN", datetime(2026, 10, 28, 7, 0)),  # standard block: 7 days
        ("OPT-OR6-20261104-1130", "S-RUIZ", datetime(2026, 10, 21, 7, 0)),  # robotic block: 14 days
    ]
    assert result.closed_dates == []


def test_d1_tuesday_fits_typical_but_runs_past_block_end_at_long_length() -> None:
    tuesday = service_at(DEMO_NOW).search_availability(D1_QUERY).options[0]
    assert tuesday.case_capacity_minutes == 120  # 150-minute window less 30 minutes turnover
    assert 112 <= tuesday.case_capacity_minutes < 135  # 15 minutes over at P80


def test_blocks_release_on_their_own_horizon() -> None:
    # Oct 21 07:00: Dr. Ruiz's robotic Wednesday releases; Dr. Chen's standard Wednesday is still held.
    result = service_at(datetime(2026, 10, 21, 7, 0)).search_availability(D1_QUERY)
    wednesday = {o.room_id: o.ownership for o in result.options + result.held if o.date == date(2026, 11, 4)}
    assert wednesday == {"OR-6": Ownership.RELEASED, "OR-5": Ownership.HELD_BY_OTHER}


def test_own_block_becomes_released_time_once_it_releases() -> None:
    result = service_at(datetime(2026, 10, 20, 7, 0)).search_availability(D1_QUERY)
    assert result.options[0].option_id == "OPT-OR5-20261103-1300"
    assert result.options[0].ownership is Ownership.RELEASED


def test_schedule_close_turns_a_date_into_an_add_on() -> None:
    # Monday Nov 2 closes at 14:00 on the business day before: Friday Oct 30.
    service = service_at(datetime(2026, 10, 30, 13, 59))
    assert date(2026, 11, 2) not in service.search_availability(D1_QUERY).closed_dates
    service = service_at(datetime(2026, 10, 30, 14, 0))
    assert service.search_availability(D1_QUERY).closed_dates == [date(2026, 11, 2)]


def test_hold_after_schedule_close_is_past_cutoff() -> None:
    clock = FrozenClock(datetime(2026, 11, 2, 13, 0))
    service = MockSchedulingService.from_fixtures(FIXTURES, clock)
    option = service.search_availability(D1_QUERY).options[0]  # Tuesday, still open
    clock.set(datetime(2026, 11, 2, 14, 0))
    with pytest.raises(PastCutoff):
        service.place_hold(option.option_id, "REQ-1")


def test_a_robot_ready_room_without_a_free_robot_is_not_offered() -> None:
    # Oct 28: both Wednesday blocks have released, so OR-5 and OR-6 both open at 11:30.
    service = service_at(datetime(2026, 10, 28, 8, 0))
    wednesday = {o.room_id: o for o in service.search_availability(D1_QUERY).options if o.date == date(2026, 11, 4)}
    assert set(wednesday) == {"OR-5", "OR-6"}

    service.place_hold(wednesday["OR-5"].option_id, "REQ-1")  # takes the only orthopedic robot

    rooms_now = {o.room_id for o in service.search_availability(D1_QUERY).options if o.date == date(2026, 11, 4)}
    assert rooms_now == set()
    with pytest.raises(ResourceConflict):
        service.place_hold(wednesday["OR-6"].option_id, "REQ-2")


def test_schedule_view_shows_blocks_cases_and_release_state() -> None:
    view = service_at(DEMO_NOW).get_schedule(DateWindow(start=date(2026, 11, 6), end=date(2026, 11, 6)))
    or5 = next(rd for rd in view.room_days if rd.room_id == "OR-5")
    assert [(s.state, s.owner_id) for s in or5.segments] == [("held", "S-CHEN"), ("released", "S-CHEN")]
    assert [c.case_id for c in or5.cases] == ["C-4440", "C-4441"]
    assert next(rd for rd in view.room_days if rd.room_id == "OR-1").segments[0].filler


def test_inconsistent_scheduling_fixtures_fail_at_startup() -> None:
    records = load_scheduling(FIXTURES)
    clash = FixtureCase(
        case_id="C-9999",
        surgeon_id="S-PATEL",
        procedure_id="TKA-ROBOTIC",
        room_id="OR-5",
        date=date(2026, 11, 3),
        start="09:00",
        end="10:00",
        assets=["ORTHO-ROBOT-1"],
    )
    broken = replace(records, booked=records.booked.model_copy(update={"cases": [*records.booked.cases, clash]}))
    with pytest.raises(FixtureError, match="overlap"):
        MockSchedulingService(broken, load_ehr(FIXTURES), FrozenClock(DEMO_NOW))
