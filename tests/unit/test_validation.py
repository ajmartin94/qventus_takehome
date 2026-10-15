"""Qualifying both requests: reading values, resolving identities, checking against the order and policy."""

from __future__ import annotations

from datetime import date

import pytest

from or_booking.domain.models import (
    AnesthesiaType,
    Authorization,
    AuthStatus,
    BookingField,
    DateWindow,
    FieldStatus,
    IssueKind,
    Laterality,
    PatientClass,
    ResolvedBy,
    Stage,
)
from or_booking.domain.validation import (
    build_booking_request,
    next_issue,
    parse_anesthesia,
    parse_date,
    parse_date_window,
    parse_laterality,
    parse_patient_class,
    qualify_booking,
    qualify_query,
    query_inputs,
    resolve_patient,
)
from tests.unit.factories import TODAY, draft, order, patient, payer, policies, procedure, surgeon

F = BookingField

# --- Reading values ----------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [("R", Laterality.RIGHT), ("right knee", Laterality.RIGHT), ("Lt", Laterality.LEFT), ("LEFT", Laterality.LEFT),
     ("b/l", Laterality.BILATERAL), ("bilateral", Laterality.BILATERAL), ("left and right", None), ("knee", None)],
)  # fmt: skip
def test_parse_laterality(text, expected) -> None:
    assert parse_laterality(text) is expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("General + nerve block", AnesthesiaType.GENERAL_WITH_NERVE_BLOCK), ("GA", AnesthesiaType.GENERAL),
     ("general", AnesthesiaType.GENERAL), ("spinal with MAC", AnesthesiaType.REGIONAL), ("MAC", AnesthesiaType.MAC),
     ("general_with_nerve_block", AnesthesiaType.GENERAL_WITH_NERVE_BLOCK), ("whatever is easiest", None)],
)  # fmt: skip
def test_parse_anesthesia(text, expected) -> None:
    assert parse_anesthesia(text) is expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("Outpatient", PatientClass.OUTPATIENT), ("extended recovery (overnight)", PatientClass.EXTENDED_RECOVERY),
     ("inpatient", PatientClass.INPATIENT), ("23 hour obs", PatientClass.EXTENDED_RECOVERY), ("tbd", None)],
)  # fmt: skip
def test_parse_patient_class(text, expected) -> None:
    assert parse_patient_class(text) is expected


@pytest.mark.parametrize(
    ("text", "past", "expected"),
    [("1958-03-12", False, date(1958, 3, 12)), ("3/12/1958", False, date(1958, 3, 12)), ("03/12/58", True, date(1958, 3, 12)),
     ("05/19/49", True, date(1949, 5, 19)), ("March 12, 1958", False, date(1958, 3, 12)), ("13/45/2020", False, None), ("soon", False, None)],
)  # fmt: skip
def test_parse_date(text, past, expected) -> None:
    assert parse_date(text, today=TODAY, past=past) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Week of 11/2 preferred", (date(2026, 11, 2), date(2026, 11, 6))),
        ("week of 2026-11-04", (date(2026, 11, 2), date(2026, 11, 6))),  # a Wednesday: its Mon-Fri
        ("2026-11-02/2026-11-06", (date(2026, 11, 2), date(2026, 11, 6))),
        ("2026-11-02 to 2026-11-13", (date(2026, 11, 2), date(2026, 11, 13))),
        ("11/2 - 11/6", (date(2026, 11, 2), date(2026, 11, 6))),
        ("11/4", (date(2026, 11, 4), date(2026, 11, 4))),
        ("1/5", (date(2027, 1, 5), date(2027, 1, 5))),  # the next January 5th
        ("as soon as possible", None),
    ],
)
def test_parse_date_window(text, expected) -> None:
    window = parse_date_window(text, TODAY)
    assert (window.start, window.end) == expected if expected else window is None


# --- Stage 1: the availability query -----------------------------------------


def test_query_qualifies_from_lookups() -> None:
    d = draft(surgeon="Dr. Priya Patel", procedure="Robotic R TKA", date_window="week of 11/2")
    q = qualify_query(d, surgeons=[surgeon()], procedures=[procedure()], today=TODAY)
    assert q.ready
    assert query_inputs(q.draft).model_dump() == {
        "surgeon_id": "S-PATEL",
        "procedure_id": "TKA-ROBOTIC",
        "window": DateWindow(start=date(2026, 11, 2), end=date(2026, 11, 6)).model_dump(),
    }
    resolved = q.draft.get(F.SURGEON)
    assert (resolved.status, resolved.stated, resolved.resolved_by) == (FieldStatus.RESOLVED, "Dr. Priya Patel", ResolvedBy.LOOKUP)


@pytest.mark.parametrize(
    ("surgeons", "procedures", "values", "expected"),
    [
        ([], [procedure()], {}, (F.SURGEON, IssueKind.NOT_FOUND)),
        ([surgeon()], [procedure(), procedure(id="TKA")], {}, (F.PROCEDURE, IssueKind.AMBIGUOUS)),  # "27447"
        ([surgeon(privileges=["TKA"])], [procedure()], {}, (F.PROCEDURE, IssueKind.NOT_PRIVILEGED)),
        ([surgeon()], [procedure()], {"date_window": "whenever"}, (F.DATE_WINDOW, IssueKind.INVALID)),
        ([surgeon()], [procedure()], {"date_window": "week of 2026-10-05"}, (F.DATE_WINDOW, IssueKind.INVALID)),  # past
    ],
)
def test_query_issues(surgeons, procedures, values, expected) -> None:
    d = draft(**{"surgeon": "Dr. Patel", "procedure": "27447", "date_window": "week of 11/2", **values})
    q = qualify_query(d, surgeons=surgeons, procedures=procedures, today=TODAY)
    assert [(i.field, i.kind) for i in q.issues] == [expected]


def test_missing_query_inputs_and_unqualified_query_refused() -> None:
    q = qualify_query(draft(), surgeons=[], procedures=[], today=TODAY)
    assert {(i.field, i.kind) for i in q.issues} == {
        (F.SURGEON, IssueKind.MISSING),
        (F.PROCEDURE, IssueKind.MISSING),
        (F.DATE_WINDOW, IssueKind.MISSING),
    }
    with pytest.raises(ValueError, match="resolved"):
        query_inputs(draft(surgeon="Dr. Patel"))  # proposed values never reach a request


# --- Stage 2: the booking request --------------------------------------------


def test_two_patients_with_the_same_name_is_ambiguous_without_revealing_them() -> None:
    q = resolve_patient(draft(patient_name="Maria Gomez"), [patient(), patient(mrn="100877", dob=date(1971, 7, 30))], TODAY)
    (issue,) = q.issues
    assert (issue.field, issue.kind, issue.candidate_count) == (F.PATIENT_DOB, IssueKind.AMBIGUOUS, 2)
    assert "100877" not in issue.detail and "1971" not in issue.detail


def test_name_and_date_of_birth_resolve_the_patient() -> None:
    q = resolve_patient(draft(patient_name="Maria Gomez", patient_dob="3/12/1958"), [patient()], TODAY)
    assert q.ready
    assert (q.draft.resolved(F.PATIENT_NAME), q.draft.resolved(F.PATIENT_DOB)) == ("100231", "1958-03-12")
    mismatch = resolve_patient(draft(patient_name="Maria Gomez", patient_dob="1/1/1990"), [patient()], TODAY)
    assert [(i.field, i.kind) for i in mismatch.issues] == [(F.PATIENT_DOB, IssueKind.NOT_FOUND)]


def _booking_draft(**overrides: str):
    values = dict(
        surgeon="Dr. Patel",
        procedure="Robotic R TKA",
        patient_name="Maria Gomez",
        patient_dob="3/12/1958",
        laterality="R",
        diagnosis="OA right knee",
        anesthesia_type="General + nerve block",
        patient_class="Outpatient",
        implants="Loaner knee set, rep to attend",
    )
    d = draft(**{**values, **overrides})
    d = qualify_query(d.propose(F.DATE_WINDOW, "week of 11/2", d.get(F.SURGEON).source), surgeons=[surgeon()], procedures=[procedure()], today=TODAY).draft
    return resolve_patient(d, [patient()], TODAY).draft


def _qualify(d, orders=None, surgery_date=date(2026, 11, 3), auth=None):
    orders = orders if orders is not None else [order(**({"authorization": auth} if auth else {}))]
    return qualify_booking(
        d, procedure=procedure(), patient=patient(), orders=orders, payer=payer(),
        policies=policies(), surgery_date=surgery_date, today=TODAY,
    )  # fmt: skip


def test_d1_style_booking_qualifies_and_takes_the_diagnosis_from_the_order() -> None:
    q = _qualify(_booking_draft())
    assert q.ready, q.issues
    diagnosis = q.draft.get(F.DIAGNOSIS)
    assert (diagnosis.value, diagnosis.stated, diagnosis.resolved_by, diagnosis.ref) == ("M17.11", "OA right knee", ResolvedBy.SURGEONS_ORDER, "ORD-1")
    assert q.draft.get(F.LATERALITY).resolved_by is ResolvedBy.SURGEONS_ORDER


def test_side_that_contradicts_the_order_is_raised_never_resolved() -> None:
    q = _qualify(_booking_draft(laterality="left"))
    (issue,) = q.issues
    assert (issue.field, issue.kind) == (F.LATERALITY, IssueKind.CONFLICTS_WITH_ORDER)
    assert "left" in issue.detail and "right" in issue.detail
    assert q.draft.get(F.LATERALITY).status is FieldStatus.PROPOSED


@pytest.mark.parametrize(
    ("change", "orders", "expected"),
    [
        ({"patient_dob": None}, None, (F.PATIENT_DOB, IssueKind.MISSING)),  # policy: two identifiers, even with one match
        ({"anesthesia_type": "whatever is easiest"}, None, (F.ANESTHESIA_TYPE, IssueKind.INVALID)),
        ({"implants": None}, None, (F.IMPLANTS, IssueKind.MISSING)),
        ({}, [], (F.DIAGNOSIS, IssueKind.NOT_FOUND)),  # no surgical order on file
        ({}, [order(procedure_id="THA")], (F.PROCEDURE, IssueKind.CONFLICTS_WITH_ORDER)),
    ],
)
def test_booking_issues(change, orders, expected) -> None:
    values = {k: v for k, v in change.items() if v is not None}
    d = _booking_draft(**values)
    for field, value in change.items():
        if value is None:
            d = d.model_copy(update={"fields": {f: fv for f, fv in d.fields.items() if f.value != field}})
    assert expected in [(i.field, i.kind) for i in _qualify(d, orders=orders).issues]


def test_authorization_gate_blocks_booking_close_to_surgery() -> None:
    (issue,) = _qualify(_booking_draft(), surgery_date=date(2026, 10, 26)).issues
    assert (issue.field, issue.kind, issue.rule_id) == (F.AUTHORIZATION, IssueKind.GATED, "auth")
    approved = Authorization(status=AuthStatus.APPROVED, number="A-1")
    assert _qualify(_booking_draft(), surgery_date=date(2026, 10, 26), auth=approved).ready


def test_next_issue_asks_query_gaps_first_then_hard_failures_then_field_order() -> None:
    q1 = qualify_query(draft(surgeon="Dr. Patel"), surgeons=[surgeon()], procedures=[], today=TODAY)
    booking = _qualify(_booking_draft(laterality="left", anesthesia_type="whatever is easiest")).issues
    assert next_issue(booking + q1.issues).stage is Stage.QUERY
    assert next_issue(q1.issues).field is F.PROCEDURE
    assert [i.field for i in booking] == [F.LATERALITY, F.ANESTHESIA_TYPE]
    assert next_issue(booking[::-1]).field is F.LATERALITY  # side before anesthesia, whatever the order raised
    assert next_issue([]) is None


def test_booking_request_is_built_only_from_resolved_values() -> None:
    q = _qualify(_booking_draft())
    request = build_booking_request(
        q.draft, option_id="OPT-OR5-20261103-1300", procedure=procedure(), scheduled_minutes=112,
        booked_by="C-0042", idempotency_key="REQ-1",
    )  # fmt: skip
    assert (request.patient_mrn, request.laterality, request.diagnosis_code) == ("100231", Laterality.RIGHT, "M17.11")
    assert (request.anesthesia_type, request.patient_class) == (AnesthesiaType.GENERAL_WITH_NERVE_BLOCK, PatientClass.OUTPATIENT)
    assert request.implants[0].vendor_id == "V-KNEE-01" and request.implants[0].loaner_set and request.authorization is None

    with pytest.raises(ValueError, match="laterality"):
        build_booking_request(
            _qualify(_booking_draft(laterality="left")).draft, option_id="x", procedure=procedure(),
            scheduled_minutes=112, booked_by="C-0042", idempotency_key="REQ-1",
        )  # fmt: skip
