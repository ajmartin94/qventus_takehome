"""Policy conditions, rule-set validation and routing: table-driven, inline rules only."""

from __future__ import annotations

import pytest

from or_booking.domain.policy import (
    RouteAction,
    Situation,
    applicable_requirements,
    case_facts,
    matches,
    route_for,
)
from tests.unit.factories import order, patient, payer, policies, procedure


@pytest.mark.parametrize(
    ("conditions", "facts", "expected"),
    [
        ({}, {}, True),  # no conditions: always applies
        ({"procedure.loaner_set": True}, {"procedure.loaner_set": True}, True),
        ({"procedure.loaner_set": True}, {"procedure.loaner_set": False}, False),
        ({"a": "x", "b": "y"}, {"a": "x", "b": "y"}, True),  # every condition must match...
        ({"a": "x", "b": "y"}, {"a": "x", "b": "z"}, False),  # ...not just one
        ({"authorization.status": ["pending", "approved"]}, {"authorization.status": "pending"}, True),  # list: any of
        ({"authorization.status": ["pending", "approved"]}, {"authorization.status": "not_started"}, False),
        ({"loaner_set.first_time": True}, {"loaner_set.first_time": None}, False),  # unknown never matches
        ({"loaner_set.first_time": True}, {}, False),
    ],
)
def test_conditions(conditions, facts, expected) -> None:
    assert matches(conditions, facts) is expected


def test_case_facts_expose_the_vocabulary_conditions_use() -> None:
    facts = case_facts(procedure=procedure(), payer=payer(), authorization=order().authorization, patient=patient())
    assert facts["procedure.laterality"] == "required"
    assert facts["procedure.loaner_set"] is True
    assert facts["payer.decision_clock.standard_days"] == 7
    assert facts["authorization.status"] == "not_started" and facts["authorization.has_number"] is False
    assert facts["loaner_set.first_time"] is None  # nobody said


def test_requirements_apply_by_procedure_attributes() -> None:
    rules = policies()
    with_side = applicable_requirements(rules, case_facts(procedure=procedure()))
    without = applicable_requirements(rules, case_facts(procedure=procedure(laterality="none", implant=None)))
    assert {r.id for r in with_side} == {"identity", "basics", "side", "implants"}
    assert {r.id for r in without} == {"identity", "basics"}


def test_policies_naming_unknown_facts_are_rejected() -> None:
    bad = [{"id": "x", "description": "x", "applies_when": {"procedure.colour": "red"}, "require": ["diagnosis"], "source": "t"}]
    with pytest.raises(ValueError, match="procedure.colour"):
        policies(booking=bad)


def test_deadline_cycles_are_rejected_but_opposite_anchor_and_wait_are_fine() -> None:
    def rule(rule_id: str, **extra) -> dict:
        return {"id": rule_id, "item": rule_id, "owner": "o", "source": "t", **extra}

    # a's deadline comes from b's, while b waits on a: legitimate (authorization and financial clearance)
    policies(readiness=[rule("a", due={"before_item": "b"}), rule("b", due={"before_surgery": {"days": 1}}, depends_on=["a"])])
    with pytest.raises(ValueError, match="cycle"):
        policies(readiness=[rule("a", due={"before_item": "b"}), rule("b", due={"before_item": "a"})])


def test_routes_come_from_policy_and_nothing_is_silently_dropped() -> None:
    rules = policies(
        routing=[
            {
                "situation": "urgent_or_emergent",
                "action": "hand_off",
                "route_to": ["anesthesiologist_in_charge", "or_desk"],
                "source": "t",
            }
        ]
    )
    urgent = route_for(rules, Situation.URGENT_OR_EMERGENT)
    assert urgent.route_to == ["anesthesiologist_in_charge", "or_desk"] and urgent.from_policy

    unruled = route_for(rules, Situation.CLINICAL_QUESTION)
    assert (unruled.action, unruled.route_to, unruled.from_policy) == (RouteAction.NEEDS_REVIEW, ["coordinator"], False)
