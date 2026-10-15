"""SchedulingService contract: what the agent relies on at this boundary, for every adapter.

Each adapter supplies a `SchedulingWorld`: the service plus enough knowledge of its data
to exercise the contract (a query that returns bookable and held windows, a booking
request for an option). The mock passes today; a real integration must pass the same
suite before it's wired in. The checks cover only the agent's side of the contract, not
the other system's internals.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime

import pytest

from or_booking.adapters.clock import FrozenClock
from or_booking.adapters.scheduling_mock import MockSchedulingService
from or_booking.domain.errors import BlockNotReleased, HoldExpired, NotPrivileged, SlotTaken
from or_booking.domain.models import (
    AnesthesiaType,
    AvailabilityQuery,
    BookingRequest,
    CaseMinutes,
    CaseStatus,
    DateWindow,
    ImplantRequest,
    Laterality,
    Ownership,
    PatientClass,
)
from or_booking.ports.scheduling import SchedulingService
from tests.conftest import DEMO_NOW, FIXTURES


@dataclass
class SchedulingWorld:
    service: SchedulingService
    now: Callable[[], datetime]
    advance_minutes: Callable[[int], None]
    hold_minutes: int
    query: AvailabilityQuery  # must return at least one bookable option and one held window
    unprivileged_query: AvailabilityQuery  # the surgeon isn't credentialed for the procedure
    booking_for: Callable[[str, str], BookingRequest]  # (option_id, idempotency_key) -> request


def northwind_mock() -> SchedulingWorld:
    clock = FrozenClock(DEMO_NOW)
    week = DateWindow(start=date(2026, 11, 2), end=date(2026, 11, 6))
    minutes = CaseMinutes(typical=112, long=135)

    def booking_for(option_id: str, key: str) -> BookingRequest:
        return BookingRequest(
            option_id=option_id,
            surgeon_id="S-PATEL",
            procedure_id="TKA-ROBOTIC",
            patient_mrn="100231",
            laterality=Laterality.RIGHT,
            diagnosis_code="M17.11",
            scheduled_minutes=112,
            anesthesia_type=AnesthesiaType.GENERAL_WITH_NERVE_BLOCK,
            patient_class=PatientClass.OUTPATIENT,
            implants=[ImplantRequest(system="Total knee system", vendor_id="V-KNEE-01", loaner_set=True, rep_attending=True)],
            booked_by="C-0042",
            idempotency_key=key,
        )

    return SchedulingWorld(
        service=MockSchedulingService.from_fixtures(FIXTURES, clock),
        now=clock.now,
        advance_minutes=lambda m: clock.advance(minutes=m),
        hold_minutes=10,
        query=AvailabilityQuery(surgeon_id="S-PATEL", procedure_id="TKA-ROBOTIC", case_minutes=minutes, window=week),
        unprivileged_query=AvailabilityQuery(surgeon_id="S-CHEN", procedure_id="TKA-ROBOTIC", case_minutes=minutes, window=week),
        booking_for=booking_for,
    )


@pytest.fixture(params=[pytest.param(northwind_mock, id="mock")])
def world(request: pytest.FixtureRequest) -> SchedulingWorld:
    return request.param()


def test_every_option_carries_its_ownership(world: SchedulingWorld) -> None:
    result = world.service.search_availability(world.query)
    assert result.options, "the contract world must offer at least one bookable option"
    for option in result.options:
        assert option.ownership in {Ownership.OWN_BLOCK, Ownership.RELEASED, Ownership.OPEN}
        if option.ownership is Ownership.OWN_BLOCK:
            assert option.block_owner_id == world.query.surgeon_id
        assert option.case_capacity_minutes >= world.query.case_minutes.typical


def test_held_windows_carry_their_release_time(world: SchedulingWorld) -> None:
    held = world.service.search_availability(world.query).held
    assert held, "the contract world must report at least one window in another owner's block"
    for window in held:
        assert window.ownership is Ownership.HELD_BY_OTHER and not window.bookable
        assert window.block_owner_id and window.block_owner_id != world.query.surgeon_id
        assert window.releases_at is not None and window.releases_at > world.now()


def test_unprivileged_surgeon_is_refused(world: SchedulingWorld) -> None:
    with pytest.raises(NotPrivileged):
        world.service.search_availability(world.unprivileged_query)


def test_hold_in_another_owners_unreleased_block_is_refused_with_release_time(world: SchedulingWorld) -> None:
    window = world.service.search_availability(world.query).held[0]
    with pytest.raises(BlockNotReleased) as refused:
        world.service.place_hold(window.option_id, "REQ-A")
    assert refused.value.releases_at == window.releases_at


def test_hold_on_a_slot_someone_else_holds_is_slot_taken(world: SchedulingWorld) -> None:
    option = world.service.search_availability(world.query).options[0]
    world.service.place_hold(option.option_id, "REQ-A")
    with pytest.raises(SlotTaken):
        world.service.place_hold(option.option_id, "REQ-B")


def test_released_or_expired_hold_frees_the_slot(world: SchedulingWorld) -> None:
    option = world.service.search_availability(world.query).options[0]
    first = world.service.place_hold(option.option_id, "REQ-A")
    world.service.release_hold(first.hold_id)
    second = world.service.place_hold(option.option_id, "REQ-B")
    world.advance_minutes(world.hold_minutes + 1)
    assert world.service.place_hold(option.option_id, "REQ-C").hold_id not in {first.hold_id, second.hold_id}


def test_confirming_twice_with_the_same_key_returns_the_same_case(world: SchedulingWorld) -> None:
    option = world.service.search_availability(world.query).options[0]
    hold = world.service.place_hold(option.option_id, "REQ-A")
    request = world.booking_for(option.option_id, "REQ-A-KEY")

    first = world.service.confirm_booking(hold.hold_id, request)
    retry = world.service.confirm_booking(hold.hold_id, request)

    assert first.status is CaseStatus.BOOKED and retry.case_id == first.case_id
    same_key = [c for c in world.service.find_cases(patient_mrn=request.patient_mrn) if c.idempotency_key == "REQ-A-KEY"]
    assert len(same_key) == 1


def test_confirming_after_the_hold_expires_is_hold_expired(world: SchedulingWorld) -> None:
    option = world.service.search_availability(world.query).options[0]
    hold = world.service.place_hold(option.option_id, "REQ-A")
    world.advance_minutes(world.hold_minutes + 1)
    with pytest.raises(HoldExpired):
        world.service.confirm_booking(hold.hold_id, world.booking_for(option.option_id, "REQ-A-KEY"))


def test_booked_time_is_no_longer_offered(world: SchedulingWorld) -> None:
    option = world.service.search_availability(world.query).options[0]
    hold = world.service.place_hold(option.option_id, "REQ-A")
    case = world.service.confirm_booking(hold.hold_id, world.booking_for(option.option_id, "REQ-A-KEY"))

    again = world.service.search_availability(world.query)
    for o in again.options:
        assert o.room_id != case.room_id or o.end <= case.start or o.start >= case.end
