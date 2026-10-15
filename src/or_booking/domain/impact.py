"""Change impact: what a change to a booked case invalidates. Stub.

Designed, not built. A real analyzer would take the booked case, its readiness list and
the proposed change, and return the items that move or break: an authorization whose
dates no longer cover the surgery, an H&P that falls outside the window, a loaner set
whose delivery deadline moves, pre-admission testing to rebook, and the notifications
each team needs. Date change is the first stretch goal (scenario D9).
"""

from __future__ import annotations

from or_booking.domain.models import BookedCase, ReadinessItem, Unsupported


def change_impact(case: BookedCase, readiness: list[ReadinessItem], change: str) -> Unsupported:
    """`change` says what is changing, e.g. "moving C-4417 to a new date"."""
    return Unsupported(
        capability="Change impact analysis",
        reason=f"Working out what {change} invalidates isn't supported in the prototype",
        would_need=["authorization dates", "H&P window", "loaner set deadline", "pre-admission testing", "notifications"],
    )
