"""Business days, readiness deadlines and statuses, booking gates, and case sizing."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from or_booking.domain.models import AuthStatus, Authorization, CaseMinutes, ReadinessStatus
from or_booking.domain.policy import Offset, case_facts
from or_booking.domain.readiness import (
    add_business_days,
    after,
    before,
    booking_gates,
    readiness_list,
    readiness_risks,
    subtract_business_days,
)
from or_booking.domain.sizing import SizingSource, override, percentile, size_case
from tests.unit.factories import NOW, TODAY, patient, payer, policies, procedure

SURGERY = datetime(2026, 11, 3, 13, 0)  # Tuesday


@pytest.mark.parametrize(
    ("start", "n", "expected"),
    [
        (date(2026, 11, 3), 1, date(2026, 11, 2)),  # Tue -> Mon
        (date(2026, 11, 2), 1, date(2026, 10, 30)),  # Mon -> Fri, over the weekend
        (date(2026, 11, 3), 3, date(2026, 10, 29)),  # Tue -> Thu the week before
        (date(2026, 11, 1), 1, date(2026, 10, 30)),  # from a Sunday
        (date(2026, 11, 3), 0, date(2026, 11, 3)),
    ],
)
def test_subtract_business_days(start, n, expected) -> None:
    assert subtract_business_days(start, n) == expected


def test_add_business_days_and_offsets() -> None:
    assert add_business_days(date(2026, 10, 30), 1) == date(2026, 11, 2)  # Fri -> Mon
    assert before(SURGERY, Offset(hours=72)) == datetime(2026, 10, 31, 13, 0)
    assert before(SURGERY, Offset(business_days=3)) == datetime(2026, 10, 29, 13, 0)  # keeps the clock time
    assert after(datetime(2026, 10, 30, 10, 0), Offset(business_days=1)) == datetime(2026, 11, 2, 10, 0)


def _rule(rule_id: str, **extra) -> dict:
    return {"id": rule_id, "item": rule_id.replace("_", " "), "owner": "Office", "source": "t", **extra}


READINESS = [
    _rule("h_and_p", dated_by="patient.h_and_p_date", valid_within={"days": 30}),
    _rule(
        "auth",
        applies_when={"payer.prior_auth": "required"},
        due={"before_item": "clearance", "lead_time_fact": "payer.decision_clock.standard_days"},
        done_when={"authorization.status": ["pending", "approved"]},
    ),
    _rule("clearance", due={"before_surgery": {"business_days": 1}, "at": "12:00"}, depends_on=["auth"]),
    _rule("chart", due={"before_surgery": {"hours": 72}}, depends_on=["h_and_p"]),
    _rule(
        "loaner",
        applies_when={"procedure.loaner_set": True},
        due={"before_surgery": {"hours": 48}},
        variants=[{"applies_when": {"loaner_set.first_time": True}, "due": {"before_surgery": {"business_days": 3}}, "label": "the set is new"}],
    ),
]


def _items(now=NOW, auth=AuthStatus.NOT_STARTED, h_and_p=None, first_time=None, **facts_extra):
    facts = case_facts(
        procedure=procedure(),
        payer=payer(),
        authorization=Authorization(status=auth),
        patient=patient(h_and_p_date=h_and_p),
        loaner_first_time=first_time,
    )
    return {i.rule_id: i for i in readiness_list(policies(readiness=READINESS), facts, SURGERY, now)}


def test_due_times_by_hours_business_days_clock_time_and_lead_time() -> None:
    items = _items()
    assert items["clearance"].due == datetime(2026, 11, 2, 12, 0)  # noon the business day before
    assert items["auth"].due == datetime(2026, 10, 26, 12, 0)  # clearance less the payer's 7 days
    assert items["chart"].due == datetime(2026, 10, 31, 13, 0)  # 72 hours
    assert items["h_and_p"].valid_from == date(2026, 10, 4) and items["h_and_p"].due is None
    assert [i for i in items] == ["h_and_p", "auth", "clearance", "chart", "loaner"]  # policy order


def test_a_matching_variant_overrides_the_base_deadline() -> None:
    assert _items()["loaner"].due == datetime(2026, 11, 1, 13, 0)
    assert "Oct 29 13:00 instead if the set is new" in _items()["loaner"].detail  # unknown: say both
    new_set = _items(first_time=True)["loaner"]
    assert new_set.due == datetime(2026, 10, 29, 13, 0) and new_set.detail == ""


@pytest.mark.parametrize(
    ("h_and_p", "status", "detail"),
    [
        (None, ReadinessStatus.OPEN, "None on file"),
        (date(2026, 10, 1), ReadinessStatus.OPEN, "On file is dated Oct 01, before Oct 04"),
        (date(2026, 10, 4), ReadinessStatus.DONE, ""),
    ],
)
def test_dated_documents_count_only_inside_the_window(h_and_p, status, detail) -> None:
    item = _items(h_and_p=h_and_p)["h_and_p"]
    assert (item.status, item.detail) == (status, detail)


def test_done_overdue_and_at_risk() -> None:
    assert _items(auth=AuthStatus.PENDING)["auth"].status is ReadinessStatus.DONE
    late = _items(now=datetime(2026, 10, 27, 9, 0))
    assert late["auth"].status is ReadinessStatus.OVERDUE
    assert late["clearance"].status is ReadinessStatus.AT_RISK  # waits on the overdue authorization
    assert readiness_risks(list(late.values())) == [
        "auth: due Mon Oct 26 12:00, already passed",
        "clearance: waits on an overdue item",
    ]


@pytest.mark.parametrize(
    ("surgery", "auth", "number", "blocks"),
    [
        (date(2026, 11, 3), AuthStatus.NOT_STARTED, None, False),  # 20 days out: gate doesn't apply
        (date(2026, 10, 26), AuthStatus.NOT_STARTED, None, True),  # 12 days out, nothing on file
        (date(2026, 10, 26), AuthStatus.PENDING, None, True),  # pending without a number isn't enough
        (date(2026, 10, 26), AuthStatus.PENDING, "A-1", False),
    ],
)
def test_authorization_gate(surgery, auth, number, blocks) -> None:
    facts = case_facts(procedure=procedure(), payer=payer(), authorization=Authorization(status=auth, number=number))
    (gate,) = booking_gates(policies(), facts, surgery, TODAY)
    assert gate.blocks_booking is blocks


# --- Sizing ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("values", "p", "expected"),
    [([100, 110, 120], 0.5, 110), ([100, 110, 120, 130], 0.5, 115), ([1, 2, 3, 4, 5], 0.8, 4), ([10], 0.8, 10)],
)
def test_percentile(values, p, expected) -> None:
    assert percentile(values, p) == expected


def test_sizing_falls_back_and_says_so() -> None:
    own = size_case([100, 105, 110, 115, 120], [], default_minutes=90)
    assert (own.source, own.minutes) == (SizingSource.SURGEON_HISTORY, CaseMinutes(typical=110, long=116))
    pooled = size_case([100, 110], [80, 90, 100, 110, 120, 130], default_minutes=90)
    assert pooled.source is SizingSource.PROCEDURE_HISTORY and "2 prior cases" in pooled.note
    default = size_case([], [80, 90], default_minutes=90)
    assert (default.source, default.minutes) == (SizingSource.PROCEDURE_DEFAULT, CaseMinutes(typical=90, long=90))


def test_override_keeps_the_estimate_beside_it() -> None:
    estimate = size_case([100, 105, 110, 115, 120], [], default_minutes=90)
    overridden = override(estimate, CaseMinutes(typical=130, long=150))
    assert overridden.source is SizingSource.OVERRIDE and overridden.estimate == estimate.minutes
