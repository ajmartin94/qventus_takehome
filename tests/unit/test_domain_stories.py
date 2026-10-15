"""Phase 2's done criterion on Northwind's data: the domain core carries D1 from fax fields to a booking.

The orchestrator (Phase 3) will run these same steps from the state machine; here each
step is called by hand, with lookups through the fixture adapters, so the story reads
top to bottom. D6 and D7 check the side conflict and the cardiac stub at domain level.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest

from or_booking.app import Services
from or_booking.domain.models import (
    AvailabilityQuery,
    BookingField,
    CaseDraft,
    CaseStatus,
    Channel,
    IssueKind,
    Ownership,
    ReadinessStatus,
    SourceKind,
    Unsupported,
)
from or_booking.domain.policy import AutonomyMode, Situation, case_facts, route_for
from or_booking.domain.ranking import rank_options, requested_day_status
from or_booking.domain.readiness import readiness_list, readiness_risks
from or_booking.domain.sizing import size_case
from or_booking.domain.straight_through import StraightThroughInputs, evaluate
from or_booking.domain.strategies import StrategyKind, select_strategy
from or_booking.domain.validation import (
    build_booking_request,
    patient_lookup_keys,
    qualify_booking,
    qualify_query,
    query_inputs,
    resolve_patient,
)
from tests.conftest import DEMO_NOW

F = BookingField
TODAY = DEMO_NOW.date()

# What the model would extract from fixtures/inbox/fax_001.txt: proposed values with evidence.
FAX_001 = {
    F.SURGEON: "Dr. Priya Patel",
    F.PATIENT_NAME: "Maria Gomez",
    F.PROCEDURE: "Robotic R TKA",
    F.LATERALITY: "R",
    F.DIAGNOSIS: "OA right knee",
    F.ANESTHESIA_TYPE: "General + nerve block",
    F.PATIENT_CLASS: "Outpatient",
    F.AUTHORIZATION: "Medicare Advantage - auth pending",
    F.IMPLANTS: "Loaner knee set, rep to attend",
    F.DATE_WINDOW: "Week of 11/2 preferred",
}


def extracted(values: dict[BookingField, str], request_id: str = "REQ-0001", channel: Channel = Channel.FAX) -> CaseDraft:
    draft = CaseDraft(request_id=request_id, channel=channel)
    for field, value in values.items():
        draft = draft.propose(field, value, SourceKind.DOCUMENT, evidence=value)
    return draft


def qualified_query(s: Services, draft: CaseDraft) -> CaseDraft:
    q = qualify_query(
        draft,
        surgeons=s.directory.find_surgeons(draft.get(F.SURGEON).stated),
        procedures=s.directory.find_procedures(draft.get(F.PROCEDURE).stated),
        today=TODAY,
    )
    assert q.ready, q.issues
    return q.draft


def test_d1_sizes_searches_and_ranks(services: Services) -> None:
    draft = qualified_query(services, extracted(FAX_001))
    surgeon = services.directory.get_surgeon(draft.resolved(F.SURGEON))
    procedure = services.directory.get_procedure(draft.resolved(F.PROCEDURE))

    sizing = size_case(
        services.duration_history.surgeon_durations(surgeon.id, procedure.id),
        services.duration_history.procedure_durations(procedure.id),
        procedure.default_minutes,
    )
    assert (sizing.minutes.typical, sizing.minutes.long, sizing.sample_size) == (112, 135, 14)

    strategy = select_strategy(procedure, surgeon, draft.stated_urgency)
    assert strategy.kind is StrategyKind.STANDARD
    query = strategy.plan(query_inputs(draft), sizing.minutes)
    assert isinstance(query, AvailabilityQuery)
    assert query.model_dump(mode="json", exclude={"preferences"}) == {  # Section 5.4, as sent
        "surgeon_id": "S-PATEL",
        "procedure_id": "TKA-ROBOTIC",
        "case_minutes": {"typical": 112, "long": 135},
        "window": {"start": "2026-11-02", "end": "2026-11-06"},
    }

    result = services.scheduling.search_availability(query)
    facts = case_facts(procedure=procedure)  # the patient isn't known yet; risk uses what is
    policies = services.policy_store.policies()
    risks = {o.option_id: readiness_risks(readiness_list(policies, facts, o.start, DEMO_NOW)) for o in result.options}
    ranked = rank_options(result.options, sizing.minutes, TODAY, risks)

    assert [(r.option.option_id, r.option.ownership, r.overrun_minutes) for r in ranked] == [
        ("OPT-OR5-20261103-1300", Ownership.OWN_BLOCK, 15),  # Tuesday, own block, 15 minutes over at P80
        ("OPT-OR6-20261105-0730", Ownership.OPEN, 0),
        ("OPT-OR5-20261106-1200", Ownership.RELEASED, 0),
    ]
    assert all(not r.readiness_risks for r in ranked)
    wednesday = requested_day_status(date(2026, 11, 4), result)
    assert wednesday.status == "held_by_other"
    assert {(w.block_owner_id, w.releases_at) for w in wednesday.held} == {
        ("S-CHEN", datetime(2026, 10, 28, 7, 0)),
        ("S-RUIZ", datetime(2026, 10, 21, 7, 0)),
    }


def test_d1_identifies_the_patient_and_builds_the_booking_request(services: Services) -> None:
    s, policies = services, services.policy_store.policies()
    draft = qualified_query(s, extracted(FAX_001))
    procedure = s.directory.get_procedure("TKA-ROBOTIC")

    # Two patients named Maria Gomez: ask for the date of birth, reveal neither
    name, dob = patient_lookup_keys(draft, TODAY)
    first = resolve_patient(draft, s.directory.find_patients(name, dob), TODAY)
    (issue,) = first.issues
    assert (issue.field, issue.kind, issue.candidate_count) == (F.PATIENT_DOB, IssueKind.AMBIGUOUS, 2)

    # The coordinator answers: "DOB 3/12/1958, take Tuesday"
    draft = draft.propose(F.PATIENT_DOB, "1958-03-12", SourceKind.COORDINATOR, evidence="DOB 3/12/1958")
    name, dob = patient_lookup_keys(draft, TODAY)
    second = resolve_patient(draft, s.directory.find_patients(name, dob), TODAY)
    assert second.ready and second.draft.resolved(F.PATIENT_NAME) == "100231"

    patient = s.directory.get_patient("100231")
    orders = s.directory.orders_for_patient(patient.mrn)
    payer = s.directory.get_payer(patient.payer_id)
    surgery_start = datetime(2026, 11, 3, 13, 0)
    booking = qualify_booking(
        second.draft, procedure=procedure, patient=patient, orders=orders, payer=payer,
        policies=policies, surgery_date=surgery_start.date(), today=TODAY,
    )  # fmt: skip
    assert booking.ready, booking.issues  # 20 days out: a pending-or-not authorization doesn't gate booking

    surgeon = s.directory.get_surgeon("S-PATEL")
    request = build_booking_request(
        booking.draft, option_id="OPT-OR5-20261103-1300", procedure=procedure, scheduled_minutes=112,
        booked_by="C-0042", idempotency_key="REQ-0001", requested_by=surgeon.office,
    )  # fmt: skip
    assert request.model_dump(mode="json", exclude={"requested_by", "authorization"}) == {  # Section 5.4
        "option_id": "OPT-OR5-20261103-1300",
        "surgeon_id": "S-PATEL",
        "procedure_id": "TKA-ROBOTIC",
        "patient_mrn": "100231",
        "laterality": "right",
        "diagnosis_code": "M17.11",
        "scheduled_minutes": 112,
        "anesthesia_type": "general_with_nerve_block",
        "patient_class": "outpatient",
        "implants": [{"system": "Total knee system", "vendor_id": "V-KNEE-01", "loaner_set": True, "rep_attending": True}],
        "booked_by": "C-0042",
        "idempotency_key": "REQ-0001",
    }

    # Readiness list (Section 4.9)
    order = orders[0]
    facts = case_facts(procedure=procedure, payer=payer, authorization=order.authorization, patient=patient)
    items = readiness_list(policies, facts, surgery_start, DEMO_NOW)
    assert [(i.rule_id, i.due, i.valid_from, i.status) for i in items] == [
        ("h_and_p", None, date(2026, 10, 4), ReadinessStatus.OPEN),
        ("prior_authorization", datetime(2026, 10, 26, 12, 0), None, ReadinessStatus.OPEN),
        ("financial_clearance", datetime(2026, 11, 2, 12, 0), None, ReadinessStatus.OPEN),
        ("chart_complete", datetime(2026, 10, 31, 13, 0), None, ReadinessStatus.OPEN),
        ("loaner_set_in_spd", datetime(2026, 11, 1, 13, 0), None, ReadinessStatus.OPEN),
        ("vendor_rep", None, None, ReadinessStatus.OPEN),
    ]
    assert items[4].detail == "Due Oct 29 13:00 instead if the set is new to the hospital"

    # Tier 3 in shadow mode: it would have qualified, and the agent still doesn't act on it
    verdict = evaluate(
        policies.autonomy_for("straight_through_booking"),
        StraightThroughInputs(
            issues=booking.issues, order_conflict=False, strategy_supported=True, ownership=Ownership.OWN_BLOCK,
            resource_conflict=False, schedule_closed=False, duration_overridden=False, duplicate=False,
        ),
    )  # fmt: skip
    assert (verdict.eligible, verdict.mode, verdict.would_act) == (True, AutonomyMode.SHADOW, False)

    # The scheduling service accepts exactly this request against a hold
    s.scheduling.search_availability(
        AvailabilityQuery.model_validate({**query_inputs(booking.draft).model_dump(), "case_minutes": {"typical": 112, "long": 135}})
    )
    hold = s.scheduling.place_hold("OPT-OR5-20261103-1300", "REQ-0001")
    case = s.scheduling.confirm_booking(hold.hold_id, request)
    assert (case.status, case.room_id, case.start, case.end) == (
        CaseStatus.BOOKED, "OR-5", datetime(2026, 11, 3, 13, 0), datetime(2026, 11, 3, 14, 52)
    )


def test_d6_left_knee_against_a_right_order_is_raised(services: Services) -> None:
    s = services
    email = extracted(
        {
            F.SURGEON: "Dr. Chen", F.PATIENT_NAME: "John Carter", F.PATIENT_DOB: "11/02/1962",
            F.PROCEDURE: "Total knee arthroplasty", F.LATERALITY: "LEFT knee", F.DIAGNOSIS: "primary OA",
            F.ANESTHESIA_TYPE: "spinal with MAC", F.PATIENT_CLASS: "outpatient",
            F.IMPLANTS: "knee system, rep attending", F.DATE_WINDOW: "2026-11-02/2026-11-06",
        },
        channel=Channel.EMAIL,
    )  # fmt: skip
    draft = qualified_query(s, email)
    name, dob = patient_lookup_keys(draft, TODAY)
    draft = resolve_patient(draft, s.directory.find_patients(name, dob), TODAY).draft
    patient = s.directory.get_patient(draft.resolved(F.PATIENT_NAME))
    booking = qualify_booking(
        draft, procedure=s.directory.get_procedure("TKA"), patient=patient, orders=s.directory.orders_for_patient(patient.mrn),
        payer=s.directory.get_payer(patient.payer_id), policies=s.policy_store.policies(), surgery_date=date(2026, 11, 2), today=TODAY,
    )  # fmt: skip
    (issue,) = booking.issues
    assert (issue.field, issue.kind) == (F.LATERALITY, IssueKind.CONFLICTS_WITH_ORDER)
    assert issue.detail == "Request says left; the surgeon's order ORD-20002 says right"


def test_d7_cardiac_case_selects_the_bed_coupled_stub_and_routes_by_policy(services: Services) -> None:
    procedure = services.directory.get_procedure("CABG")
    strategy = select_strategy(procedure, services.directory.get_surgeon("S-LEE"))
    assert strategy.kind is StrategyKind.BED_COUPLED
    draft = qualified_query(
        services, extracted({F.SURGEON: "Dr. Lee", F.PROCEDURE: "CABG", F.DATE_WINDOW: "week of 11/2"})
    )
    stub = strategy.plan(query_inputs(draft), size_case([], [], procedure.default_minutes).minutes)
    assert isinstance(stub, Unsupported) and stub.capability == "OR plus ICU bed booking"
    route = route_for(services.policy_store.policies(), Situation.UNSUPPORTED_BOOKING_STRATEGY)
    assert route.route_to == ["coordinator"] and route.from_policy


@pytest.mark.parametrize(
    ("surgeon", "procedure", "expected_source"),
    [("S-CHEN", "TKA", "surgeon_history"), ("S-PATEL", "TKA", "procedure_history"), ("S-PATEL", "UKA-ROBOTIC", "procedure_default")],
)
def test_sizing_fallbacks_on_northwind_history(services: Services, surgeon, procedure, expected_source) -> None:
    record = services.directory.get_procedure(procedure)
    sizing = size_case(
        services.duration_history.surgeon_durations(surgeon, procedure),
        services.duration_history.procedure_durations(procedure),
        record.default_minutes,
    )
    assert sizing.source.value == expected_source
    if procedure == "TKA":
        assert sizing.minutes.typical == 98
