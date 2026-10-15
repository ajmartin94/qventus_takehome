"""Small inline records for domain tests. No fixture files: each test states the facts it needs."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from or_booking.domain.models import (
    Authorization,
    AuthStatus,
    BookingField,
    CaseDraft,
    Channel,
    Contact,
    DecisionClock,
    Diagnosis,
    ImplantSpec,
    Laterality,
    Ownership,
    Patient,
    Payer,
    PostOpDestination,
    PriorAuth,
    Procedure,
    SlotOption,
    SourceKind,
    Surgeon,
    SurgicalOrder,
)
from or_booking.domain.policy import HospitalPolicies

TODAY = date(2026, 10, 14)
NOW = datetime(2026, 10, 14, 9, 0)


def surgeon(**overrides: Any) -> Surgeon:
    base = dict(
        id="S-PATEL",
        first_name="Priya",
        last_name="Patel",
        service="Orthopedics",
        privileges=["TKA-ROBOTIC", "THA"],
        office=Contact(name="Patel office", phone="555-0142", fax="555-0143"),
    )
    return Surgeon(**{**base, **overrides})


def procedure(**overrides: Any) -> Procedure:
    base = dict(
        id="TKA-ROBOTIC",
        name="Robotic-assisted total knee arthroplasty",
        cpt="27447",
        laterality="required",
        room_capabilities=["robot_ready"],
        shared_assets=["orthopedic_robot"],
        implant=ImplantSpec(system="Total knee system", vendor_id="V-KNEE-01", vendor_name="Meridian", loaner_set=True, rep_attends=True),
        post_op=PostOpDestination.SAME_DAY_OR_OVERNIGHT,
        prior_auth=PriorAuth.REQUIRED,
        default_minutes=120,
    )
    return Procedure(**{**base, **overrides})


def patient(**overrides: Any) -> Patient:
    base = dict(mrn="100231", first_name="Maria", last_name="Gomez", dob=date(1958, 3, 12), sex="F", payer_id="PAY-MA")
    return Patient(**{**base, **overrides})


def order(**overrides: Any) -> SurgicalOrder:
    base = dict(
        id="ORD-1",
        patient_mrn="100231",
        surgeon_id="S-PATEL",
        procedure_id="TKA-ROBOTIC",
        laterality=Laterality.RIGHT,
        diagnosis=Diagnosis(code="M17.11", description="Unilateral primary osteoarthritis, right knee"),
        authorization=Authorization(status=AuthStatus.NOT_STARTED),
        ordered_on=date(2026, 10, 9),
    )
    return SurgicalOrder(**{**base, **overrides})


def payer(**overrides: Any) -> Payer:
    base = dict(
        id="PAY-MA",
        name="Medicare Advantage",
        kind="medicare_advantage",
        prior_auth=PriorAuth.REQUIRED,
        decision_clock=DecisionClock(standard_days=7, expedited_hours=72),
    )
    return Payer(**{**base, **overrides})


def policies(**overrides: Any) -> HospitalPolicies:
    """A small Northwind-like rule set: two identifiers, side matching the order, an auth gate."""
    base: dict[str, Any] = dict(
        booking=[
            {"id": "identity", "description": "Name and date of birth", "require": ["patient_name", "patient_dob"], "source": "t"},
            {"id": "basics", "description": "Diagnosis, anesthesia, class", "require": ["diagnosis", "anesthesia_type", "patient_class"], "source": "t"},
            {
                "id": "side",
                "description": "Side stated and matching the order",
                "applies_when": {"procedure.laterality": "required"},
                "require": ["laterality"],
                "must_match_order": True,
                "source": "t",
            },
            {"id": "implants", "description": "Implants recorded", "applies_when": {"procedure.has_implant": True}, "require": ["implants"], "source": "t"},
        ],
        readiness=[
            {
                "id": "auth",
                "item": "Prior authorization submitted",
                "owner": "Office",
                "applies_when": {"procedure.prior_auth": "required", "payer.prior_auth": "required"},
                "done_when": {"authorization.status": ["pending", "approved"]},
                "gates_booking": {
                    "within_days_of_surgery": 14,
                    "satisfied_when": {"authorization.status": ["pending", "approved"], "authorization.has_number": True},
                    "asks_for": "authorization",
                },
                "source": "t",
            }
        ],
        routing=[],
        autonomy=[],
    )
    return HospitalPolicies.model_validate({**base, **overrides})


def draft(channel: Channel = Channel.FAX, **values: str) -> CaseDraft:
    """A draft with proposed values, as the model would extract them: draft(surgeon='Dr. Patel', ...)."""
    d = CaseDraft(request_id="REQ-1", channel=channel)
    for name, value in values.items():
        d = d.propose(BookingField(name), value, SourceKind.DOCUMENT, evidence=value)
    return d


def option(
    start: datetime,
    end: datetime,
    ownership: Ownership = Ownership.OPEN,
    room: str = "OR-5",
    turnover: int = 30,
    **extra: Any,
) -> SlotOption:
    return SlotOption(
        option_id=f"OPT-{room.replace('-', '')}-{start:%Y%m%d-%H%M}",
        room_id=room,
        start=start,
        end=end,
        turnover_minutes=turnover,
        ownership=ownership,
        **extra,
    )
