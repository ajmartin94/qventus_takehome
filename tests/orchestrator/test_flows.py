"""The state machine end to end with the scripted model (Section 6.8).

Every transition in the table is exercised by at least one flow, and a test fails if one
isn't. Each flow guarantee has its own test.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from or_booking.domain.models import AnesthesiaType, BookingField, CaseStatus, FieldStatus, IssueKind
from or_booking.orchestrator.states import State
from or_booking.orchestrator.transitions import TRANSITIONS, IllegalTransition, transition
from or_booking.ports.audit_log import AuditKind
from tests.orchestrator import harness as flows
from tests.orchestrator.harness import Harness, names, turn

F = BookingField


@pytest.fixture
def h() -> Harness:
    return Harness()


# --- The happy path ----------------------------------------------------------


def test_d1_fax_to_booking(h: Harness) -> None:
    presenting = flows.d1_presenting(h)
    assert names(presenting) == ["Intake", "Matching", "Collecting", "Searching", "Presenting"]
    (options,) = presenting.reply.cards
    assert [o.option_id for o in options.options] == ["OPT-OR5-20261103-1300", "OPT-OR6-20261105-0730", "OPT-OR5-20261106-1200"]
    assert options.still_needed == ["patient's date of birth (2 patients match the name)"]

    confirming = h.reply(presenting, "DOB 3/12/1958, take Tuesday", turn("select_option", option=1, patient_dob="1958-03-12"))
    assert names(confirming) == ["Holding", "Completing", "Confirming"] and confirming.waiting
    card = confirming.reply.cards[0]
    assert card.hold_expires == "09:10" and "would qualify (not acted on)" in card.straight_through
    assert {r.field: r.source for r in card.rows}["Side"] == "document, matches surgeon's order ORD-20001"

    booked = h.reply(confirming, "confirm", turn("confirm"))
    assert names(booked) == ["Committing", "Booked"]
    case = h.services.scheduling.get_case("C-5001")
    assert (case.patient_mrn, case.room_id, f"{case.start:%a %H:%M}") == ("100231", "OR-5", "Tue 13:00")
    assert [r.case_id for r in h.services.readiness_handoff.handoffs()] == ["C-5001"]
    assert [d.message.recipient_role for d in h.services.outbox.drafts("REQ-0001")] == ["surgeons_office"]


# --- Clarifying, parking and handing off -------------------------------------


def test_a_query_gap_is_asked_and_answered_in_chat(h: Harness) -> None:
    asked, answered = flows.query_gap_answered(h)
    assert asked.state is State.CLARIFYING and asked.reply.message == "Which dates should I look at?"
    assert names(answered) == ["Collecting", "Searching", "Presenting"]


def test_a_booking_gap_is_asked_after_the_hold(h: Harness) -> None:
    asked, answered = flows.booking_gap_answered(h)
    assert names(asked) == ["Holding", "Completing", "Clarifying"]
    assert asked.reply.message == "More than one patient matches that name. What is the patient's date of birth?"
    assert names(answered) == ["Completing", "Confirming"]


def test_three_failed_attempts_hand_off_to_the_coordinator(h: Harness) -> None:
    result = flows.attempts_exhausted(h)
    assert result.state is State.HANDED_OFF
    session = h.agent.session(result.request_id)
    assert session.attempts["date_window"] == 4 and session.route.route_to == ["coordinator"]


def test_a_hard_rule_failure_hands_off_without_asking(h: Harness) -> None:
    result = flows.hard_rule(h)
    assert names(result)[-2:] == ["Collecting", "HandedOff"]
    assert "not privileged for TKA-ROBOTIC" in result.reply.message


def test_unattended_request_asks_the_office_and_resumes_on_a_late_reply(h: Harness) -> None:
    parked, resumed = flows.unattended_reply(h)
    assert names(parked)[-2:] == ["Clarifying", "AwaitingReply"]
    assert resumed.request_id == parked.request_id  # the fax continued the same request
    assert names(resumed)[0] == "Collecting" and resumed.reply.message.startswith("Matched to open request REQ-0001.")
    session = h.agent.session(parked.request_id)
    assert session.draft.get(F.PATIENT_DOB).value == "1949-05-19"
    # The reply gave the date of birth but not the dates, so the office is asked again, the way the request came in
    drafts = h.services.outbox.drafts(parked.request_id)
    assert [(d.message.recipient_role, d.message.channel.value) for d in drafts] == [("requester", "email"), ("requester", "email")]
    assert session.state is State.AWAITING_REPLY


def test_no_reply_by_the_policy_deadline_hands_off(h: Harness) -> None:
    (result,) = flows.reply_deadline(h)
    assert names(result) == ["HandedOff"] and "No reply by Thu Oct 15 13:30" in result.reply.message


# --- Searching, presenting and holding ---------------------------------------


def test_no_bookable_time_waitlists(h: Harness) -> None:
    result = flows.wednesday_only(h)
    assert names(result)[-2:] == ["Searching", "Waitlisted"]
    assert "other owners' unreleased blocks" in h.agent.session(result.request_id).route_reason


def test_opened_time_reoffers_a_waitlisted_request(h: Harness) -> None:
    (result,) = flows.time_opened(h)
    assert names(result) == ["EventReceived", "Presenting"]
    session = h.agent.session(result.request_id)
    assert session.parent_request_id == "REQ-0001"
    assert [(r.option.room_id, r.option.ownership.value) for r in session.ranked] == [("OR-6", "released")]


def test_unsupported_strategy_routes_by_policy(h: Harness) -> None:
    result = flows.cardiac(h)
    assert names(result)[-2:] == ["Searching", "RoutedOut"]
    assert result.reply.cards[0].route_to == ["coordinator"] and "ICU" in result.reply.cards[0].reason


def test_another_owners_block_drafts_a_release_request_then_waitlists(h: Harness) -> None:
    asked, waitlisted = flows.other_owners_block(h)
    assert asked.state is State.PRESENTING and names(asked) == []  # options still offered (policy: agent continues)
    assert "releases Wed Oct 21 07:00" in asked.reply.message
    assert [d.message.recipient_role for d in h.services.outbox.drafts("REQ-0001")] == ["block_owner", "block_owner"]
    assert names(waitlisted) == ["Waitlisted"]


def test_a_slot_taken_between_search_and_pick_searches_again(h: Harness) -> None:
    result = flows.slot_taken(h)
    assert names(result) == ["Holding", "Searching", "Presenting"]
    assert "SLOT_TAKEN" in result.reply.message
    assert "OPT-OR5-20261103-1300" not in [r.option.option_id for r in h.agent.session(result.request_id).ranked]


# --- Confirming and committing -----------------------------------------------


def test_a_correction_on_the_card_goes_back_through_completing(h: Harness) -> None:
    result = flows.correction(h)
    assert names(result) == ["Completing", "Confirming"]
    assert h.agent.session(result.request_id).draft.resolved(F.ANESTHESIA_TYPE) == "general"


def test_an_expired_hold_is_reheld_and_confirmed_again(h: Harness) -> None:
    reheld, booked = flows.hold_expired(h)
    assert names(reheld) == ["Committing", "Holding", "Completing", "Confirming"]
    assert names(booked) == ["Committing", "Booked"]
    assert len([c for c in h.services.scheduling.find_cases(patient_mrn="100231")]) == 1


# --- Requests that don't book ------------------------------------------------


def test_urgent_requests_route_to_the_aic_and_or_desk(h: Harness) -> None:
    result = flows.urgent(h)
    assert names(result) == ["Intake", "Matching", "RoutedOut"]
    card = result.reply.cards[0]
    assert card.route_to == ["anesthesiologist_in_charge", "or_desk"]
    assert ("Stated urgency", "urgent") in card.fields
    assert [d.message.recipient_role for d in h.services.outbox.drafts(result.request_id)] == ["anesthesiologist_in_charge", "or_desk"]


def test_status_question_is_answered_read_only(h: Harness) -> None:
    result = flows.status_question(h)
    assert names(result)[-1] == "Answered"
    assert result.reply.message == "C-5001 is booked: Tue Nov 3, OR-5, 13:00-14:52. 6 readiness items still open."


def test_cancellation_needs_a_reason_and_confirmation(h: Harness) -> None:
    asked, cancelled = flows.cancellation(h)
    assert names(asked)[-1] == "Cancelling" and asked.waiting
    assert names(cancelled) == ["Cancelled"]
    assert h.services.scheduling.get_case("C-5001").status is CaseStatus.CANCELLED


def test_a_change_that_keeps_the_slot_updates_the_case(h: Harness) -> None:
    asked, updated = flows.modification(h)
    assert names(asked) == ["Intake", "Matching", "CaseLoaded", "Completing", "Confirming"]
    assert names(updated) == ["Committing", "Booked"]
    case = h.services.scheduling.get_case("C-5001")
    assert case.anesthesia_type is AnesthesiaType.GENERAL and f"{case.start:%a %H:%M}" == "Tue 13:00"


def test_a_displaced_case_is_rebooked(h: Harness) -> None:
    asked, presenting, confirming, booked = flows.displaced(h)
    assert names(asked) == ["EventReceived", "CaseLoaded", "Collecting", "Clarifying"]
    assert names(booked) == ["Committing", "Booked"]
    case = h.services.scheduling.get_case("C-4417")
    assert (case.case_id, f"{case.start:%a %b %d %H:%M}", case.status) == ("C-4417", "Tue Nov 10 07:30", CaseStatus.BOOKED)


# --- The flow's guarantees ---------------------------------------------------


def test_every_transition_in_the_table_is_exercised() -> None:
    covered: set[tuple[str, str]] = set()
    for flow in flows.ALL_FLOWS:
        harness = Harness()
        flow(harness)
        covered |= harness.transitions()
    table = {(t.source.value, t.target.value) for t in TRANSITIONS}
    assert table - covered == set(), "transitions no flow exercises"
    assert covered - table == set(), "transitions taken that aren't in the table"


def test_only_confirming_leads_to_committing() -> None:
    assert [t.source for t in TRANSITIONS if t.target is State.COMMITTING] == [State.CONFIRMING]
    with pytest.raises(IllegalTransition):
        transition(State.PRESENTING, State.COMMITTING)


def test_every_transition_is_recorded(h: Harness) -> None:
    result = flows.d1_booked(h)
    session = h.agent.session(result.request_id)
    recorded = [e.name for e in h.audit.entries(result.request_id) if e.kind is AuditKind.TRANSITION]
    assert len(recorded) == len(session.path) == 10
    calls = {e.name for e in h.audit.entries(result.request_id) if e.kind is AuditKind.PORT_CALL}
    assert {"scheduling.search_availability", "scheduling.place_hold", "scheduling.confirm_booking"} <= calls
    models = [e.detail for e in h.audit.entries(result.request_id) if e.kind is AuditKind.MODEL_CALL]
    assert [(m["prompt"], m["version"]) for m in models][:2] == [("extract_document", "v1"), ("explain_options", "v1")]


def test_model_values_stay_proposed_until_a_lookup_resolves_them(h: Harness) -> None:
    extraction = {**(flows.D1.scripted_extraction or {})}
    extraction["mentions"] = [m for m in extraction["mentions"] if m["field"] != "surgeon"] + [
        {"field": "surgeon", "value": "Dr. Nobody", "evidence": "Surgeon: Dr. Nobody"}
    ]
    result = h.document("fax_001", extraction)
    session = h.agent.session(result.request_id)
    assert result.state is State.CLARIFYING
    assert session.open_question.kind is IssueKind.NOT_FOUND and session.draft.get(F.SURGEON).status is FieldStatus.PROPOSED
    assert session.booking_request is None


def test_an_intent_that_doesnt_fit_the_state_doesnt_move_it(h: Harness) -> None:
    presenting = flows.d1_presenting(h)
    result = h.reply(presenting, "confirm", turn("confirm"))  # nothing to confirm while options are on screen
    assert result.state is State.PRESENTING and names(result) == []


def test_urgency_mid_conversation_is_noted_not_acted_on(h: Harness) -> None:
    presenting = flows.d1_presenting(h)
    result = h.reply(presenting, "actually this is urgent", turn("urgent_request", urgency="urgent"))
    assert result.state is State.PRESENTING and "anesthesiologist_in_charge" in result.reply.message


def test_sessions_survive_in_the_store(h: Harness) -> None:
    result = flows.d1_confirming(h)
    reloaded = h.agent.session(result.request_id)
    assert reloaded.state is State.CONFIRMING and reloaded.hold is not None
    assert reloaded.created_at == datetime(2026, 10, 14, 9, 0)
