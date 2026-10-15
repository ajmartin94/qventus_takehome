"""The hospital's structured policies: four rule types (Section 2.4 of the implementation plan).

The agent implements rule *types*; a hospital supplies however many rules of those
types it has, as data read through the `PolicyStore` port. Nothing here names a
hospital or a value: Northwind's rules live in `fixtures/policies/`.

Conditions use a deliberately small language: `applies_when` maps a fact name to an
allowed value (or list of allowed values), and every entry must match. There are no
expressions and no code in policy files. Facts the code exposes look like
`procedure.laterality`, `procedure.loaner_set`, `payer.prior_auth` or
`loaner_set.first_time`.
"""

from __future__ import annotations

from datetime import time
from enum import StrEnum

from pydantic import model_validator

from or_booking.domain.models import BookingField, Model

Scalar = str | int | bool
Conditions = dict[str, Scalar | list[Scalar]]


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
    to another item's deadline, less a lead time read from a fact (for example the
    payer's decision clock).
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
    """The item must be satisfied before booking a surgery this close."""

    within_days_of_surgery: int


class ReadinessVariant(Model):
    applies_when: Conditions
    due: Deadline


class ReadinessRule(Model):
    id: str
    item: str
    owner: str
    applies_when: Conditions = {}
    due: Deadline | None = None
    valid_within: Offset | None = None  # a document must be dated no earlier than surgery minus this
    done_when: Conditions = {}
    gates_booking: BookingGate | None = None
    depends_on: list[str] = []
    variants: list[ReadinessVariant] = []
    source: str


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
        for rule in self.readiness:
            refs = list(rule.depends_on)
            refs += [d.before_item for d in [rule.due, *(v.due for v in rule.variants)] if d and d.before_item]
            unknown = [r for r in refs if r not in readiness_ids]
            if unknown:
                raise ValueError(f"readiness rule {rule.id} refers to unknown items {unknown}")
        return self

    def routing_for(self, situation: Situation) -> RoutingRule | None:
        return next((r for r in self.routing if r.situation == situation), None)

    def autonomy_for(self, action: str) -> AutonomyRule | None:
        return next((r for r in self.autonomy if r.action == action), None)
