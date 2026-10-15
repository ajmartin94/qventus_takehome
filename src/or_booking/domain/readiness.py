"""Readiness list: what must be in place before surgery, who owns it and when it's due (Section 5.7).

Every item comes from a hospital readiness rule that applies to the case. Due times are
computed back from the surgery start in hours, calendar days or business days
(Monday to Friday; holidays aren't modelled), at the rule's clock time if it has one,
or back from another item's deadline less a lead time (the payer's decision clock).

Status:
- `done`: the facts show it (an authorization pending, an H&P dated inside the window)
- `overdue`: the due time has passed
- `at_risk`: something it waits on is overdue or at risk
- `open`: otherwise
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime, timedelta

from or_booking.domain.models import Model, ReadinessItem, ReadinessStatus
from or_booking.domain.policy import Deadline, Facts, HospitalPolicies, Offset, ReadinessRule, matches, unknown_facts

# ---------------------------------------------------------------------------
# Calendar arithmetic
# ---------------------------------------------------------------------------


def subtract_business_days(day: date, n: int) -> date:
    while n > 0:
        day -= timedelta(days=1)
        n -= day.weekday() < 5
    return day


def add_business_days(day: date, n: int) -> date:
    while n > 0:
        day += timedelta(days=1)
        n -= day.weekday() < 5
    return day


def before(moment: datetime, offset: Offset) -> datetime:
    """`moment` minus an offset; business days keep the clock time."""
    if offset.business_days:
        return datetime.combine(subtract_business_days(moment.date(), offset.business_days), moment.time())
    return moment - timedelta(hours=offset.hours, days=offset.days)


def after(moment: datetime, offset: Offset) -> datetime:
    """`moment` plus an offset, e.g. a reply deadline one business day after a question."""
    if offset.business_days:
        return datetime.combine(add_business_days(moment.date(), offset.business_days), moment.time())
    return moment + timedelta(hours=offset.hours, days=offset.days)


# ---------------------------------------------------------------------------
# Readiness list
# ---------------------------------------------------------------------------


def readiness_list(policies: HospitalPolicies, facts: Facts, surgery_start: datetime, now: datetime) -> list[ReadinessItem]:
    rules = {r.id: r for r in policies.readiness if matches(r.applies_when, facts)}
    dues: dict[str, datetime | None] = {}

    def due_of(rule_id: str) -> datetime | None:
        if rule_id not in dues:
            rule = rules.get(rule_id)
            dues[rule_id] = _deadline(_effective_due(rule, facts), surgery_start, facts, due_of) if rule else None
        return dues[rule_id]

    items: dict[str, ReadinessItem] = {}

    def build(rule: ReadinessRule) -> ReadinessItem:
        if rule.id in items:
            return items[rule.id]
        waits_on = [build(rules[d]) for d in rule.depends_on if d in rules]
        due = due_of(rule.id)
        valid_from = before(surgery_start, rule.valid_within).date() if rule.valid_within else None
        done = bool(rule.done_when) and matches(rule.done_when, facts)
        detail = ""
        if rule.dated_by:
            dated = facts.get(rule.dated_by)
            done = dated is not None and valid_from is not None and dated >= valid_from
            if dated is None:
                detail = "None on file"
            elif not done:
                detail = f"On file is dated {dated:%b %d}, before {valid_from:%b %d}"
        if done:
            status = ReadinessStatus.DONE
        elif due is not None and now >= due:
            status = ReadinessStatus.OVERDUE
        elif any(w.status in (ReadinessStatus.OVERDUE, ReadinessStatus.AT_RISK) for w in waits_on):
            status = ReadinessStatus.AT_RISK
            detail = "Waits on an item that is overdue or at risk"
        else:
            status = ReadinessStatus.OPEN
        notes = [detail] if detail else []
        notes += _variant_notes(rule, facts, surgery_start, due_of)
        items[rule.id] = ReadinessItem(
            rule_id=rule.id,
            item=rule.item,
            owner=rule.owner,
            due=due,
            valid_from=valid_from,
            status=status,
            depends_on=[d for d in rule.depends_on if d in rules],
            detail="; ".join(notes),
        )
        return items[rule.id]

    return [build(rule) for rule in rules.values()]


def readiness_risks(items: list[ReadinessItem]) -> list[str]:
    """What a ranked option shows as readiness risk for its date."""
    risks = []
    for i in items:
        if i.status is ReadinessStatus.OVERDUE and i.due:
            risks.append(f"{i.item}: due {i.due:%a %b %d %H:%M}, already passed")
        elif i.status is ReadinessStatus.AT_RISK:
            risks.append(f"{i.item}: waits on an overdue item")
    return risks


def _effective_due(rule: ReadinessRule, facts: Facts) -> Deadline | None:
    return next((v.due for v in rule.variants if matches(v.applies_when, facts)), rule.due)


DueOf = Callable[[str], datetime | None]


def _deadline(deadline: Deadline | None, surgery_start: datetime, facts: Facts, due_of: DueOf) -> datetime | None:
    if deadline is None:
        return None
    if deadline.before_surgery is not None:
        moment = before(surgery_start, deadline.before_surgery)
    else:
        assert deadline.before_item is not None
        anchor = due_of(deadline.before_item)
        if anchor is None:  # the item it's anchored to doesn't apply to this case
            return None
        lead = facts.get(deadline.lead_time_fact) if deadline.lead_time_fact else None
        moment = anchor - timedelta(days=lead or 0)
    return datetime.combine(moment.date(), deadline.at) if deadline.at else moment


def _variant_notes(rule: ReadinessRule, facts: Facts, surgery_start: datetime, due_of: DueOf) -> list[str]:
    """When a variant hinges on a fact nobody has stated yet, say what the due time would be."""
    notes = []
    for variant in rule.variants:
        if unknown_facts(variant.applies_when, facts):
            alt = _deadline(variant.due, surgery_start, facts, due_of)
            if alt is not None:
                notes.append(f"Due {alt:%b %d %H:%M} instead if {variant.label or 'its condition holds'}")
    return notes


# ---------------------------------------------------------------------------
# Booking gates
# ---------------------------------------------------------------------------


class GateResult(Model):
    rule_id: str
    item: str
    within_days_of_surgery: int
    days_until_surgery: int
    satisfied: bool

    @property
    def applies(self) -> bool:
        return self.days_until_surgery <= self.within_days_of_surgery

    @property
    def blocks_booking(self) -> bool:
        return self.applies and not self.satisfied


def booking_gates(policies: HospitalPolicies, facts: Facts, surgery_date: date, today: date) -> list[GateResult]:
    """Readiness rules that gate booking itself, checked with the booking request."""
    return [
        GateResult(
            rule_id=r.id,
            item=r.item,
            within_days_of_surgery=r.gates_booking.within_days_of_surgery,
            days_until_surgery=(surgery_date - today).days,
            satisfied=matches(r.gates_booking.satisfied_when, facts),
        )
        for r in policies.readiness
        if r.gates_booking and matches(r.applies_when, facts)
    ]
