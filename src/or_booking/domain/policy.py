"""The hospital's structured policies: four rule types (Section 2.4 of the implementation plan).

The agent implements rule *types*; a hospital supplies however many rules of those
types it has, as data read through the `PolicyStore` port. Nothing here names a
hospital or a value: Northwind's rules live in `fixtures/policies/`.

Conditions use a deliberately small language: `applies_when` maps a fact name to an
allowed value (or list of allowed values), and every entry must match. There are no
expressions and no code in policy files. The facts a condition may name are the closed
vocabulary in `FACTS`; a policy file naming any other fact is rejected when it loads.
Anything a hospital needs beyond that is a new fact in the code, or a "needs review"
route to a person.
"""

from __future__ import annotations

from datetime import time
from enum import StrEnum
from typing import Any

from pydantic import model_validator

from or_booking.domain.models import Authorization, BookingField, Model, Patient, Payer, Procedure

Scalar = str | int | bool
Conditions = dict[str, Scalar | list[Scalar]]
Facts = dict[str, Any]  # fact name -> value; None when unknown

# The facts conditions can test, and what each means. `case_facts` computes them.
FACTS: dict[str, str] = {
    "procedure.id": "Procedure master id",
    "procedure.laterality": "'required' or 'none'",
    "procedure.has_implant": "Whether the procedure uses an implant",
    "procedure.loaner_set": "Whether the implant comes as a vendor loaner set",
    "procedure.rep_attends": "Whether a vendor representative attends",
    "procedure.prior_auth": "Whether the procedure usually needs authorization: required, not_required, varies",
    "procedure.post_op": "Post-op destination: same_day, same_day_or_overnight, overnight, inpatient, icu",
    "procedure.tandem_eligible": "Whether the procedure can run in paired rooms",
    "payer.kind": "medicare, medicare_advantage, commercial or medicaid",
    "payer.prior_auth": "Whether the payer requires authorization for elective surgery",
    "payer.decision_clock.standard_days": "Days the payer has for a standard authorization decision",
    "payer.decision_clock.expedited_hours": "Hours the payer has for an expedited decision",
    "authorization.status": "not_started, pending, approved or denied, from the surgeon's order",
    "authorization.has_number": "Whether an authorization reference number is on file",
    "patient.h_and_p_date": "Date of the most recent history and physical on file",
    "loaner_set.first_time": "Whether the loaner set is new to the hospital",
    "request.urgency": "Urgency as the requester stated it: none, urgent or emergent",
}


def matches(conditions: Conditions, facts: Facts) -> bool:
    """Every condition must hold. An unknown fact (None) never matches."""
    for name, allowed in conditions.items():
        value = facts.get(name)
        if value is None or value not in (allowed if isinstance(allowed, list) else [allowed]):
            return False
    return True


def unknown_facts(conditions: Conditions, facts: Facts) -> list[str]:
    return [name for name in conditions if facts.get(name) is None]


def case_facts(
    *,
    procedure: Procedure | None = None,
    payer: Payer | None = None,
    authorization: Authorization | None = None,
    patient: Patient | None = None,
    loaner_first_time: bool | None = None,
    urgency: str = "none",
) -> Facts:
    """The fact vocabulary for one case, from the records the orchestrator looked up."""
    clock = payer.decision_clock if payer else None
    return {
        "procedure.id": procedure.id if procedure else None,
        "procedure.laterality": procedure.laterality if procedure else None,
        "procedure.has_implant": procedure.implant is not None if procedure else None,
        "procedure.loaner_set": bool(procedure.implant and procedure.implant.loaner_set) if procedure else None,
        "procedure.rep_attends": bool(procedure.implant and procedure.implant.rep_attends) if procedure else None,
        "procedure.prior_auth": procedure.prior_auth.value if procedure else None,
        "procedure.post_op": procedure.post_op.value if procedure else None,
        "procedure.tandem_eligible": procedure.tandem_eligible if procedure else None,
        "payer.kind": payer.kind if payer else None,
        "payer.prior_auth": payer.prior_auth.value if payer else None,
        "payer.decision_clock.standard_days": clock.standard_days if clock else None,
        "payer.decision_clock.expedited_hours": clock.expedited_hours if clock else None,
        "authorization.status": authorization.status.value if authorization else None,
        "authorization.has_number": bool(authorization.number) if authorization else None,
        "patient.h_and_p_date": patient.h_and_p_date if patient else None,
        "loaner_set.first_time": loaner_first_time,
        "request.urgency": urgency,
    }


class Offset(Model):
    """A span before surgery, in hours, calendar days or business days (Mon-Fri)."""

    hours: int = 0
    days: int = 0
    business_days: int = 0

    @model_validator(mode="after")
    def _one_unit(self) -> Offset:
        if sum(1 for v in (self.hours, self.days, self.business_days) if v) != 1:
            raise ValueError("an offset uses exactly one of hours, days or business_days")
        return self


class Deadline(Model):
    """When a readiness item is due.

    Either a span before surgery (optionally at a clock time on that day), or relative
    to another item's deadline, less a lead time in days read from a fact (for example
    the payer's decision clock).
    """

    before_surgery: Offset | None = None
    at: time | None = None
    before_item: str | None = None
    lead_time_fact: str | None = None

    @model_validator(mode="after")
    def _one_anchor(self) -> Deadline:
        if (self.before_surgery is None) == (self.before_item is None):
            raise ValueError("a deadline is anchored to exactly one of before_surgery or before_item")
        return self


# ---------------------------------------------------------------------------
# Rule type 1: required booking data
# ---------------------------------------------------------------------------


class BookingRequirement(Model):
    id: str
    description: str
    applies_when: Conditions = {}
    require: list[BookingField]
    must_match_order: bool = False  # the value must agree with the surgeon's order
    source: str


# ---------------------------------------------------------------------------
# Rule type 2: readiness requirement
# ---------------------------------------------------------------------------


class BookingGate(Model):
    """Booking a surgery this close requires `satisfied_when` to hold (checked with the booking request)."""

    within_days_of_surgery: int
    satisfied_when: Conditions
    asks_for: BookingField  # what to ask the requester for when the gate blocks


class ReadinessVariant(Model):
    applies_when: Conditions
    due: Deadline
    label: str = ""  # how a person would say the condition, e.g. "the set is new to the hospital"


class ReadinessRule(Model):
    id: str
    item: str
    owner: str
    applies_when: Conditions = {}
    due: Deadline | None = None
    # A dated document (the fact `dated_by`) counts only if dated no earlier than surgery minus `valid_within`.
    dated_by: str | None = None
    valid_within: Offset | None = None
    done_when: Conditions = {}
    gates_booking: BookingGate | None = None
    depends_on: list[str] = []
    variants: list[ReadinessVariant] = []
    source: str

    @model_validator(mode="after")
    def _dated_pair(self) -> ReadinessRule:
        if (self.dated_by is None) != (self.valid_within is None):
            raise ValueError(f"readiness rule {self.id}: dated_by and valid_within go together")
        return self


# ---------------------------------------------------------------------------
# Rule type 3: routing
# ---------------------------------------------------------------------------


class Situation(StrEnum):
    """The closed set of situations the code detects. Policy decides who handles each."""

    URGENT_OR_EMERGENT = "urgent_or_emergent"
    ADD_ON_AFTER_CLOSE = "add_on_after_close"
    BUMP_REQUEST = "bump_request"
    CLINICAL_QUESTION = "clinical_question"
    OTHER_OWNER_UNRELEASED_BLOCK = "other_owner_unreleased_block"
    UNSUPPORTED_BOOKING_STRATEGY = "unsupported_booking_strategy"
    UNRESOLVABLE_CONFLICT = "unresolvable_conflict"
    CLARIFICATION_UNANSWERED = "clarification_unanswered"
    CLARIFICATION_ATTEMPTS_EXHAUSTED = "clarification_attempts_exhausted"
    READINESS_UPDATE = "readiness_update"
    HUMAN_REQUESTED = "human_requested"
    AMBIGUOUS_MATCH = "ambiguous_match"  # an input could belong to more than one request or case


class RouteAction(StrEnum):
    HAND_OFF = "hand_off"  # structured handoff; the agent stops
    DECLINE_AND_ROUTE = "decline_and_route"  # the agent doesn't answer; says who will
    DRAFT_RELEASE_REQUEST = "draft_release_request"  # the agent drafts, a person sends
    LIST_AFFECTED_CASES = "list_affected_cases"  # the agent informs, a person decides
    AGENT_PROCEEDS = "agent_proceeds"
    NEEDS_REVIEW = "needs_review"  # no rule fits cleanly: a person looks


class RoutingRule(Model):
    situation: Situation
    action: RouteAction
    route_to: list[str] = []
    handoff_fields: list[str] = []
    agent_continues: bool = False
    sent_by: str | None = None
    reply_deadline: Offset | None = None
    source: str


# ---------------------------------------------------------------------------
# Rule type 4: autonomy
# ---------------------------------------------------------------------------


class AutonomyMode(StrEnum):
    ACTIVE = "active"
    SHADOW = "shadow"  # evaluate and report, never act
    DISABLED = "disabled"


class StraightThroughCheck(StrEnum):
    """Named eligibility checks the code implements; a hospital picks which apply."""

    ALL_FIELDS_RESOLVED = "all_fields_resolved"
    NO_ORDER_CONFLICT = "no_order_conflict"
    SUPPORTED_STRATEGY = "supported_strategy"
    OWN_BLOCK_OR_OPEN_TIME = "own_block_or_open_time"
    NO_RESOURCE_CONFLICT = "no_resource_conflict"
    BEFORE_SCHEDULE_CLOSE = "before_schedule_close"
    DURATION_NOT_OVERRIDDEN = "duration_not_overridden"
    NOT_DUPLICATE = "not_duplicate"


class AutonomyRule(Model):
    action: str
    tier: int
    mode: AutonomyMode = AutonomyMode.ACTIVE
    conditions: list[StraightThroughCheck] = []
    description: str

    @model_validator(mode="after")
    def _tier_range(self) -> AutonomyRule:
        if self.tier not in (1, 2, 3):
            raise ValueError("autonomy tier must be 1, 2 or 3")
        return self


# ---------------------------------------------------------------------------
# A hospital's full rule set
# ---------------------------------------------------------------------------


class HospitalPolicies(Model):
    booking: list[BookingRequirement]
    readiness: list[ReadinessRule]
    routing: list[RoutingRule]
    autonomy: list[AutonomyRule]

    @model_validator(mode="after")
    def _consistent(self) -> HospitalPolicies:
        for kind, ids in (
            ("booking", [r.id for r in self.booking]),
            ("readiness", [r.id for r in self.readiness]),
            ("routing", [r.situation for r in self.routing]),
            ("autonomy", [r.action for r in self.autonomy]),
        ):
            duplicates = {i for i in ids if ids.count(i) > 1}
            if duplicates:
                raise ValueError(f"duplicate {kind} rules: {sorted(duplicates)}")
        readiness_ids = {r.id for r in self.readiness}
        # Two separate graphs, each acyclic: deadlines anchored to another item's deadline, and
        # items waiting on others. They may point opposite ways (authorization's deadline comes
        # from financial clearance's, while financial clearance waits on authorization).
        anchors: dict[str, set[str]] = {}
        waits: dict[str, set[str]] = {}
        for rule in self.readiness:
            deadlines = [d for d in [rule.due, *(v.due for v in rule.variants)] if d]
            anchors[rule.id] = {d.before_item for d in deadlines if d.before_item}
            waits[rule.id] = set(rule.depends_on)
            unknown = [r for r in anchors[rule.id] | waits[rule.id] if r not in readiness_ids]
            if unknown:
                raise ValueError(f"readiness rule {rule.id} refers to unknown items {unknown}")
        _reject_cycles(anchors)
        _reject_cycles(waits)
        named = [name for conds in self._all_conditions() for name in conds]
        named += [r.dated_by for r in self.readiness if r.dated_by]
        named += [d.lead_time_fact for r in self.readiness for d in [r.due, *(v.due for v in r.variants)] if d and d.lead_time_fact]
        unknown_names = sorted({n for n in named if n not in FACTS})
        if unknown_names:
            raise ValueError(f"policies name facts the agent doesn't know: {unknown_names}")
        return self

    def _all_conditions(self) -> list[Conditions]:
        conds: list[Conditions] = [r.applies_when for r in self.booking]
        for r in self.readiness:
            conds += [r.applies_when, r.done_when, *(v.applies_when for v in r.variants)]
            if r.gates_booking:
                conds.append(r.gates_booking.satisfied_when)
        return conds

    def routing_for(self, situation: Situation) -> RoutingRule | None:
        return next((r for r in self.routing if r.situation == situation), None)

    def autonomy_for(self, action: str) -> AutonomyRule | None:
        return next((r for r in self.autonomy if r.action == action), None)


def _reject_cycles(edges: dict[str, set[str]]) -> None:
    done: set[str] = set()

    def visit(node: str, path: tuple[str, ...]) -> None:
        if node in path:
            raise ValueError(f"readiness items form a cycle: {' -> '.join((*path, node))}")
        if node not in done:
            for nxt in edges.get(node, ()):
                visit(nxt, (*path, node))
            done.add(node)

    for node in edges:
        visit(node, ())


# ---------------------------------------------------------------------------
# Applying the rules
# ---------------------------------------------------------------------------


def applicable_requirements(policies: HospitalPolicies, facts: Facts) -> list[BookingRequirement]:
    return [r for r in policies.booking if matches(r.applies_when, facts)]


class Route(Model):
    """Who handles a situation and what the handoff carries, as the hospital's routing policy says."""

    situation: Situation
    action: RouteAction
    route_to: list[str]
    handoff_fields: list[str] = []
    agent_continues: bool = False
    sent_by: str | None = None
    source: str
    from_policy: bool = True


def route_for(policies: HospitalPolicies, situation: Situation) -> Route:
    """The hospital's route for a situation. With no rule for it, the flow's own default applies:
    nothing is silently ignored; the coordinator reviews it."""
    rule = policies.routing_for(situation)
    if rule is None:
        return Route(
            situation=situation,
            action=RouteAction.NEEDS_REVIEW,
            route_to=["coordinator"],
            source="no hospital routing rule for this situation",
            from_policy=False,
        )
    return Route(
        situation=rule.situation,
        action=rule.action,
        route_to=rule.route_to,
        handoff_fields=rule.handoff_fields,
        agent_continues=rule.agent_continues,
        sent_by=rule.sent_by,
        source=rule.source,
    )
