"""Typed errors shared by the domain and the ports.

A port raises one of these instead of a generic failure, so a `SlotTaken` from the
mock scheduling service means exactly what it would mean from a real integration,
and the orchestrator handles each one by name. Every error carries a stable `code`
and structured `details` for the audit log.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, ClassVar


class BookingError(Exception):
    """Base class for every typed error a port or the domain may raise."""

    code: ClassVar[str] = "BOOKING_ERROR"

    def __init__(self, message: str, **details: Any) -> None:
        super().__init__(message)
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        def plain(value: Any) -> Any:
            return value.isoformat() if isinstance(value, (date, datetime)) else value

        return {"code": self.code, "message": self.message, **{k: plain(v) for k, v in self.details.items()}}


class SlotTaken(BookingError):
    """The chosen time was booked or held by someone else after it was offered."""

    code = "SLOT_TAKEN"

    def __init__(self, option_id: str, detail: str = "") -> None:
        super().__init__(f"Option {option_id} is no longer free. {detail}".strip(), option_id=option_id)
        self.option_id = option_id


class HoldExpired(BookingError):
    """The hold protecting a slot ran out before the booking was confirmed."""

    code = "HOLD_EXPIRED"

    def __init__(self, hold_id: str, expired_at: datetime) -> None:
        super().__init__(f"Hold {hold_id} expired at {expired_at:%H:%M}.", hold_id=hold_id, expired_at=expired_at)
        self.hold_id = hold_id
        self.expired_at = expired_at


class BlockNotReleased(BookingError):
    """The time belongs to another owner's block that has not been released yet."""

    code = "BLOCK_NOT_RELEASED"

    def __init__(self, option_id: str, owner_id: str, owner_name: str, releases_at: datetime | None) -> None:
        when = f"releases {releases_at:%a %b %d %H:%M}" if releases_at else "has no automatic release"
        super().__init__(
            f"Option {option_id} is in {owner_name}'s block, which {when}.",
            option_id=option_id,
            owner_id=owner_id,
            owner_name=owner_name,
            releases_at=releases_at,
        )
        self.option_id = option_id
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.releases_at = releases_at


class ResourceConflict(BookingError):
    """A room, surgeon or shared asset (robot, C-arm) is already committed at that time."""

    code = "RESOURCE_CONFLICT"

    def __init__(self, resource: str, detail: str = "") -> None:
        super().__init__(f"{resource} is not available. {detail}".strip(), resource=resource)
        self.resource = resource


class PastCutoff(BookingError):
    """The schedule for that date has closed; later requests are add-ons."""

    code = "PAST_CUTOFF"

    def __init__(self, surgery_date: date, closed_at: datetime) -> None:
        super().__init__(
            f"The schedule for {surgery_date:%a %b %d} closed at {closed_at:%a %b %d %H:%M}.",
            surgery_date=surgery_date,
            closed_at=closed_at,
        )
        self.surgery_date = surgery_date
        self.closed_at = closed_at


class NotPrivileged(BookingError):
    """The surgeon is not credentialed for the procedure."""

    code = "NOT_PRIVILEGED"

    def __init__(self, surgeon_id: str, procedure_id: str) -> None:
        super().__init__(
            f"{surgeon_id} is not privileged for {procedure_id}.", surgeon_id=surgeon_id, procedure_id=procedure_id
        )
        self.surgeon_id = surgeon_id
        self.procedure_id = procedure_id


class MissingRequiredField(BookingError):
    """A request lacks data the receiving system requires."""

    code = "MISSING_REQUIRED_FIELD"

    def __init__(self, fields: list[str]) -> None:
        super().__init__(f"Missing required fields: {', '.join(fields)}.", fields=fields)
        self.fields = fields


class RequestRejected(BookingError):
    """The request is inconsistent with what it refers to (for example, a hold for a different option)."""

    code = "REQUEST_REJECTED"

    def __init__(self, reason: str) -> None:
        super().__init__(reason, reason=reason)
        self.reason = reason


class NotFound(BookingError):
    """A referenced record (option, hold, case, patient...) does not exist."""

    code = "NOT_FOUND"

    def __init__(self, kind: str, key: str) -> None:
        super().__init__(f"No {kind} {key!r}.", kind=kind, key=key)
        self.kind = kind
        self.key = key


class NotSupportedInPrototype(BookingError):
    """A capability that is designed but stubbed. Never a silent success.

    Names who the request routes to instead, so the orchestrator can hand it off.
    """

    code = "NOT_SUPPORTED"

    def __init__(self, capability: str, routes_to: str, detail: str) -> None:
        super().__init__(
            f"{capability} is not supported in the prototype; routes to {routes_to}. {detail}".strip(),
            capability=capability,
            routes_to=routes_to,
            detail=detail,
        )
        self.capability = capability
        self.routes_to = routes_to
        self.detail = detail
