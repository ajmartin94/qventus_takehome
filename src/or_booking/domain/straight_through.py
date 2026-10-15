"""Tier 3 eligibility: would this request have qualified for booking without the coordinator?

The hospital's autonomy policy names which checks apply and whether the result is acted
on. At Northwind it runs in shadow mode: the verdict is recorded on the confirmation card
and in the audit log, and agreement with the coordinator's actual decisions is how a
hospital would earn the confidence to switch it on.
"""

from __future__ import annotations

from or_booking.domain.models import Issue, Model, Ownership
from or_booking.domain.policy import AutonomyMode, AutonomyRule, StraightThroughCheck


class StraightThroughInputs(Model):
    issues: list[Issue]  # anything still open on the draft
    order_conflict: bool
    strategy_supported: bool
    ownership: Ownership
    resource_conflict: bool
    schedule_closed: bool
    duration_overridden: bool
    duplicate: bool


class StraightThroughVerdict(Model):
    eligible: bool
    mode: AutonomyMode
    failed: list[StraightThroughCheck] = []

    @property
    def would_act(self) -> bool:
        return self.eligible and self.mode is AutonomyMode.ACTIVE


_CHECKS = {
    StraightThroughCheck.ALL_FIELDS_RESOLVED: lambda i: not i.issues,
    StraightThroughCheck.NO_ORDER_CONFLICT: lambda i: not i.order_conflict,
    StraightThroughCheck.SUPPORTED_STRATEGY: lambda i: i.strategy_supported,
    StraightThroughCheck.OWN_BLOCK_OR_OPEN_TIME: lambda i: i.ownership in (Ownership.OWN_BLOCK, Ownership.OPEN),
    StraightThroughCheck.NO_RESOURCE_CONFLICT: lambda i: not i.resource_conflict,
    StraightThroughCheck.BEFORE_SCHEDULE_CLOSE: lambda i: not i.schedule_closed,
    StraightThroughCheck.DURATION_NOT_OVERRIDDEN: lambda i: not i.duration_overridden,
    StraightThroughCheck.NOT_DUPLICATE: lambda i: not i.duplicate,
}


def evaluate(rule: AutonomyRule | None, inputs: StraightThroughInputs) -> StraightThroughVerdict:
    """No rule, or a disabled one, means not eligible: autonomy is promoted, never assumed."""
    if rule is None or rule.mode is AutonomyMode.DISABLED:
        return StraightThroughVerdict(eligible=False, mode=AutonomyMode.DISABLED)
    failed = [check for check in rule.conditions if not _CHECKS[check](inputs)]
    return StraightThroughVerdict(eligible=not failed, mode=rule.mode, failed=failed)
