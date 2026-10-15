"""Ranking, strategy selection, request matching and the Tier 3 shadow check."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from or_booking.domain.matching import MatchKind, match_request
from or_booking.domain.models import (
    AvailabilityQuery,
    AvailabilityResult,
    BookedCase,
    BookingField,
    CaseMinutes,
    CaseStatus,
    Channel,
    DateWindow,
    OptionGroup,
    Ownership,
    PostOpDestination,
    ResolvedBy,
    Unsupported,
)
from or_booking.domain.policy import AutonomyMode, AutonomyRule, StraightThroughCheck
from or_booking.domain.ranking import rank_options, requested_day_status
from or_booking.domain.straight_through import StraightThroughInputs, evaluate
from or_booking.domain.strategies import StrategyKind, select_strategy
from or_booking.domain.validation import QueryInputs
from tests.unit.factories import TODAY, draft, option, procedure, surgeon

F = BookingField
MINUTES = CaseMinutes(typical=112, long=135)


def at(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, day, hour, minute)


# --- Ranking -----------------------------------------------------------------


def test_own_block_first_then_long_fits_then_typical_only() -> None:
    options = [
        option(at(2, 12, 0), at(2, 14, 30), Ownership.OPEN, room="OR-3"),  # 150 - 30 turnover: typical only
        option(at(5, 7, 30), at(5, 11, 30), Ownership.OPEN, room="OR-6"),  # 240: fits long
        option(at(3, 13, 0), at(3, 15, 30), Ownership.OWN_BLOCK, block_owner_id="S-PATEL"),  # 150, own
        option(at(6, 12, 0), at(6, 15, 30), Ownership.RELEASED),  # 210: fits long, later
    ]
    ranked = rank_options(options, MINUTES, TODAY)
    assert [(r.option.date.day, r.group) for r in ranked] == [
        (3, OptionGroup.OWN_BLOCK),
        (5, OptionGroup.FITS_LONG),
        (6, OptionGroup.FITS_LONG),
    ]  # three at most: Monday's typical-only option is cut
    tuesday = ranked[0]
    assert (tuesday.fits_long, tuesday.overrun_minutes, tuesday.counts_toward_block, tuesday.days_until_surgery) == (False, 15, True, 20)
    assert rank_options(options, MINUTES, TODAY, limit=4)[3].group is OptionGroup.FITS_TYPICAL_ONLY


def test_held_and_too_short_windows_are_never_ranked_and_risks_attach() -> None:
    held = option(at(4, 11, 30), at(4, 15, 30), Ownership.HELD_BY_OTHER)
    short = option(at(2, 13, 0), at(2, 15, 0), Ownership.OPEN)  # 120 - 30 turnover < 112
    ok = option(at(5, 7, 30), at(5, 11, 30), Ownership.OPEN)
    ranked = rank_options([held, short, ok], MINUTES, TODAY, readiness_risks={ok.option_id: ["H&P: overdue"]})
    assert [r.option.option_id for r in ranked] == [ok.option_id] and ranked[0].readiness_risks == ["H&P: overdue"]


def test_a_requested_day_that_isnt_offered_says_why() -> None:
    query = AvailabilityQuery(
        surgeon_id="S-PATEL", procedure_id="TKA-ROBOTIC", case_minutes=MINUTES,
        window=DateWindow(start=date(2026, 11, 2), end=date(2026, 11, 6)),
    )  # fmt: skip
    held = option(at(4, 11, 30), at(4, 15, 30), Ownership.HELD_BY_OTHER, releases_at=datetime(2026, 10, 21, 7, 0))
    result = AvailabilityResult(query=query, options=[option(at(3, 13, 0), at(3, 15, 30))], held=[held], closed_dates=[date(2026, 11, 2)])
    assert requested_day_status(date(2026, 11, 3), result).status == "bookable"
    wednesday = requested_day_status(date(2026, 11, 4), result)
    assert wednesday.status == "held_by_other" and wednesday.held[0].releases_at == datetime(2026, 10, 21, 7, 0)
    assert requested_day_status(date(2026, 11, 2), result).status == "schedule_closed"
    assert requested_day_status(date(2026, 11, 6), result).status == "no_fit"


# --- Strategies --------------------------------------------------------------


@pytest.mark.parametrize(
    ("proc", "doc", "urgency", "expected"),
    [
        (procedure(), surgeon(), "none", StrategyKind.STANDARD),
        (procedure(id="CABG", post_op=PostOpDestination.ICU), surgeon(), "none", StrategyKind.BED_COUPLED),
        (procedure(id="CATARACT", tandem_eligible=True), surgeon(runs_paired_rooms=True), "none", StrategyKind.TANDEM),
        (procedure(id="CATARACT", tandem_eligible=True), surgeon(), "none", StrategyKind.STANDARD),  # no paired rooms
        (procedure(id="TIBIA-NAIL"), surgeon(), "urgent", StrategyKind.RESERVE_AND_PREEMPT),
        (procedure(id="CABG", post_op=PostOpDestination.ICU), surgeon(), "emergent", StrategyKind.RESERVE_AND_PREEMPT),
    ],
)
def test_strategy_follows_procedure_attributes(proc, doc, urgency, expected) -> None:
    assert select_strategy(proc, doc, urgency).kind is expected


def test_only_standard_builds_a_query_and_stubs_say_why() -> None:
    inputs = QueryInputs(surgeon_id="S-LEE", procedure_id="CABG", window=DateWindow(start=date(2026, 11, 2), end=date(2026, 11, 6)))
    query = select_strategy(procedure(), surgeon()).plan(inputs, MINUTES)
    assert isinstance(query, AvailabilityQuery) and query.case_minutes == MINUTES
    stub = select_strategy(procedure(id="CABG", post_op=PostOpDestination.ICU), surgeon()).plan(inputs, MINUTES)
    assert isinstance(stub, Unsupported) and "ICU" in stub.reason and "ICU bed for the post-op nights" in stub.would_need


# --- Matching ----------------------------------------------------------------


def _resolved(d, field, value):
    return d.set(field, d.get(field).resolve(value, ResolvedBy.LOOKUP))


def test_late_reply_continues_the_open_draft() -> None:
    waiting = draft(surgeon="Dr. Priya Patel", procedure="L THA", patient_name="Aisha Rahman")
    reply = draft(Channel.FAX, surgeon="Dr. Patel", patient_name="Aisha Rahman", patient_dob="05/19/1949")
    reply = reply.model_copy(update={"request_id": "REQ-2"})
    result = match_request(reply, [waiting], [])
    assert (result.kind, result.request_id) == (MatchKind.CONTINUATION, "REQ-1") and "patient_dob" in result.reason


def test_same_request_twice_is_a_duplicate_and_strangers_are_new() -> None:
    first = draft(surgeon="Dr. Patel", patient_name="Maria Gomez", procedure="Robotic R TKA")
    again = first.model_copy(update={"request_id": "REQ-2"})
    assert match_request(again, [first], []).kind is MatchKind.DUPLICATE
    other = draft(surgeon="Dr. Chen", patient_name="John Carter").model_copy(update={"request_id": "REQ-3"})
    assert match_request(other, [first], []).kind is MatchKind.NEW


def test_requests_about_booked_cases() -> None:
    case = BookedCase(
        case_id="C-5001", status=CaseStatus.BOOKED, surgeon_id="S-PATEL", procedure_id="TKA-ROBOTIC",
        room_id="OR-5", start=at(3, 13), end=at(3, 14, 52), patient_mrn="100231",
    )  # fmt: skip
    by_number = draft(case_number="c-5001")
    assert (match_request(by_number, [], [case]).kind, match_request(by_number, [], [case]).case_id) == (MatchKind.BOOKED_CASE, "C-5001")
    assert match_request(draft(case_number="C-9999"), [], [case]).kind is MatchKind.AMBIGUOUS

    status_call = _resolved(draft(patient_name="Maria Gomez"), F.PATIENT_NAME, "100231")
    assert match_request(status_call, [], [case]).case_id == "C-5001"
    other_patient = _resolved(draft(patient_name="Maria Gomez"), F.PATIENT_NAME, "100877")
    assert match_request(other_patient, [], [case]).kind is MatchKind.NEW


def test_two_open_drafts_for_one_patient_go_to_the_coordinator() -> None:
    a = draft(patient_name="Maria Gomez")
    b = a.model_copy(update={"request_id": "REQ-2"})
    incoming = draft(patient_name="Maria Gomez", patient_dob="3/12/1958").model_copy(update={"request_id": "REQ-3"})
    result = match_request(incoming, [a, b], [])
    assert result.kind is MatchKind.AMBIGUOUS and result.candidates == ["REQ-1", "REQ-2"]


# --- Tier 3, shadow mode -----------------------------------------------------

SHADOW = AutonomyRule(action="straight_through_booking", tier=3, mode=AutonomyMode.SHADOW, conditions=list(StraightThroughCheck), description="t")


def _inputs(**overrides) -> StraightThroughInputs:
    base = dict(issues=[], order_conflict=False, strategy_supported=True, ownership=Ownership.OWN_BLOCK,
                resource_conflict=False, schedule_closed=False, duration_overridden=False, duplicate=False)  # fmt: skip
    return StraightThroughInputs(**{**base, **overrides})


def test_shadow_mode_reports_eligibility_but_never_acts() -> None:
    verdict = evaluate(SHADOW, _inputs())
    assert verdict.eligible and not verdict.would_act
    released = evaluate(SHADOW, _inputs(ownership=Ownership.RELEASED, duration_overridden=True))
    assert released.failed == [StraightThroughCheck.OWN_BLOCK_OR_OPEN_TIME, StraightThroughCheck.DURATION_NOT_OVERRIDDEN]
    assert evaluate(None, _inputs()).mode is AutonomyMode.DISABLED and not evaluate(None, _inputs()).eligible
