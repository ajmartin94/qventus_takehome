"""What the coordinator sees (Section 6.6): cards built from state, never from model prose.

Cards are plain data. The CLI renders them as Rich panels and tables; a Streamlit view
or a transcript renders the same data. The model writes at most the line above them.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import Field

from or_booking.domain.models import (
    BookingField,
    CaseDraft,
    FieldValue,
    Model,
    Ownership,
    RankedOption,
    ReadinessItem,
    ResolvedBy,
    SourceKind,
)
from or_booking.domain.sizing import CaseSizing


class OptionCard(Model):
    number: int
    option_id: str
    day: str
    room: str
    window: str
    ownership: str
    counts_toward_block: bool
    fit: str
    days_until_surgery: int
    readiness_risks: list[str] = []


class OptionsCard(Model):
    kind: Literal["options"] = "options"
    title: str
    sizing: str
    options: list[OptionCard]
    still_needed: list[str] = []


class FieldRow(Model):
    field: str
    value: str
    source: str


class ConfirmationCard(Model):
    kind: Literal["confirmation"] = "confirmation"
    title: str
    slot: str
    rows: list[FieldRow]
    hold_expires: str | None = None
    straight_through: str = ""


class OutcomeCard(Model):
    kind: Literal["outcome"] = "outcome"
    title: str
    rows: list[tuple[str, str]]
    readiness: list[ReadinessItem] = []
    drafts: list[str] = []


class HandoffCard(Model):
    kind: Literal["handoff"] = "handoff"
    title: str
    route_to: list[str]
    action: str
    reason: str
    policy: str
    fields: list[tuple[str, str]] = []


class AnswerCard(Model):
    kind: Literal["answer"] = "answer"
    title: str
    rows: list[tuple[str, str]]
    readiness: list[ReadinessItem] = []


Card = Annotated[OptionsCard | ConfirmationCard | OutcomeCard | HandoffCard | AnswerCard, Field(discriminator="kind")]


class Reply(Model):
    message: str = ""
    cards: list[Card] = []


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

FIELD_LABELS: dict[BookingField, str] = {
    BookingField.SURGEON: "Surgeon",
    BookingField.PROCEDURE: "Procedure",
    BookingField.LATERALITY: "Side",
    BookingField.DATE_WINDOW: "Dates",
    BookingField.PATIENT_NAME: "Patient",
    BookingField.PATIENT_DOB: "Date of birth",
    BookingField.DIAGNOSIS: "Diagnosis",
    BookingField.ANESTHESIA_TYPE: "Anesthesia",
    BookingField.PATIENT_CLASS: "Patient class",
    BookingField.IMPLANTS: "Implants",
    BookingField.AUTHORIZATION: "Authorization (as stated)",
    BookingField.PREFERENCES: "Preferences",
    BookingField.CASE_NUMBER: "Case number",
    BookingField.CONTACT: "Contact",
}

_SOURCE = {
    SourceKind.COORDINATOR: "coordinator",
    SourceKind.DOCUMENT: "document",
    SourceKind.SURGEONS_ORDER: "surgeon's order",
    SourceKind.PROCEDURE_MASTER: "procedure master",
    SourceKind.BOOKED_CASE: "booked case",
}
_CHECKED = {
    ResolvedBy.LOOKUP: "looked up",
    ResolvedBy.SURGEONS_ORDER: "matches surgeon's order",
    ResolvedBy.VALIDATION: "validated",
}


def day_label(d: date | datetime) -> str:
    return f"{d:%a %b} {d.day}"


def time_label(t: datetime) -> str:
    return f"{t:%H:%M}"


def provenance(fv: FieldValue) -> str:
    source = _SOURCE[fv.source]
    if fv.resolved_by is None:
        return f"{source} (not checked)"
    checked = _CHECKED[fv.resolved_by] + (f" {fv.ref}" if fv.ref and fv.resolved_by is ResolvedBy.SURGEONS_ORDER else "")
    return f"{source}, {checked}"


def field_rows(draft: CaseDraft, display: dict[BookingField, str], fields: list[BookingField]) -> list[FieldRow]:
    """One row per field: what it says, and where it came from and how it was checked."""
    rows = []
    for field in fields:
        fv = draft.get(field)
        if fv is None:
            continue
        rows.append(FieldRow(field=FIELD_LABELS[field], value=display.get(field, fv.value), source=provenance(fv)))
    return rows


def ownership_label(r: RankedOption) -> str:
    o = r.option
    if o.ownership is Ownership.OWN_BLOCK:
        return f"{o.block_owner_name}'s block"
    if o.ownership is Ownership.RELEASED:
        when = f" on {day_label(o.released_at)}" if o.released_at else ""
        return f"Released by {o.block_owner_name}{when}" if o.block_owner_name else "Released time"
    return "Open time"


def option_card(r: RankedOption, sizing: CaseSizing) -> OptionCard:
    typical, long = sizing.minutes.typical, sizing.minutes.long
    fit = f"Fits at {typical} and {long} min" if r.fits_long else f"Fits at {typical} min; {r.overrun_minutes} min past the window at {long}"
    o = r.option
    return OptionCard(
        number=r.rank,
        option_id=o.option_id,
        day=day_label(o.start),
        room=o.room_id,
        window=f"{time_label(o.start)}-{time_label(o.end)}",
        ownership=ownership_label(r),
        counts_toward_block=r.counts_toward_block,
        fit=fit,
        days_until_surgery=r.days_until_surgery,
        readiness_risks=r.readiness_risks,
    )


def option_line(r: RankedOption) -> str:
    """How an option is described to the interpretation prompt."""
    o = r.option
    return f"{day_label(o.start)}, {o.room_id}, {time_label(o.start)}-{time_label(o.end)}, {ownership_label(r).lower()}"
