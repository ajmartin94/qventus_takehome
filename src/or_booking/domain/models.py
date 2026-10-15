"""Core models: the facts the agent reasons about and the shape of its requests.

Pure data (Pydantic v2), no I/O. Two groups:

- Reference records, as a hospital's EHR, credentialing and procedure master hold them
  (surgeons, procedures, patients, surgical orders, payers).
- The agent's side of the scheduling contract (Section 5.4 of the implementation plan):
  the availability query, the options that come back, holds, the booking request and
  the booked case.

Models are frozen and reject unknown fields, so a malformed fixture or adapter
response fails when it is loaded, not halfway through a conversation.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, model_validator


class Model(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------


class Laterality(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    BILATERAL = "bilateral"


class PostOpDestination(StrEnum):
    SAME_DAY = "same_day"
    SAME_DAY_OR_OVERNIGHT = "same_day_or_overnight"
    OVERNIGHT = "overnight"
    INPATIENT = "inpatient"
    ICU = "icu"


class PriorAuth(StrEnum):
    REQUIRED = "required"
    NOT_REQUIRED = "not_required"
    VARIES = "varies"


class AuthStatus(StrEnum):
    NOT_STARTED = "not_started"
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


class AnesthesiaType(StrEnum):
    GENERAL = "general"
    GENERAL_WITH_NERVE_BLOCK = "general_with_nerve_block"
    REGIONAL = "regional"
    MAC = "mac"
    LOCAL = "local"


class PatientClass(StrEnum):
    OUTPATIENT = "outpatient"
    EXTENDED_RECOVERY = "extended_recovery"
    INPATIENT = "inpatient"


class Channel(StrEnum):
    CHAT = "chat"
    FAX = "fax"
    EMAIL = "email"
    CALL_TRANSCRIPT = "call_transcript"
    PORTAL = "portal"


class BookingField(StrEnum):
    """Every field a request can carry. Shared by the domain, the policies and the prompts.

    `FIELD_DEFINITIONS` below is the single definition of each field; the prompts'
    field list is generated from it, so the model, the validators and the cards agree.
    """

    SURGEON = "surgeon"
    PROCEDURE = "procedure"
    LATERALITY = "laterality"
    DATE_WINDOW = "date_window"
    PATIENT_NAME = "patient_name"
    PATIENT_DOB = "patient_dob"
    DIAGNOSIS = "diagnosis"
    ANESTHESIA_TYPE = "anesthesia_type"
    PATIENT_CLASS = "patient_class"
    IMPLANTS = "implants"
    AUTHORIZATION = "authorization"
    PREFERENCES = "preferences"
    CASE_NUMBER = "case_number"
    CONTACT = "contact"


FIELD_DEFINITIONS: dict[BookingField, str] = {
    BookingField.SURGEON: "The operating surgeon, as named (for example 'Dr. Priya Patel' or 'Patel').",
    BookingField.PROCEDURE: "The operation, as written, including approach (for example 'robotic R TKA').",
    BookingField.LATERALITY: "The operative side: left, right or bilateral. Spelled out, never inferred.",
    BookingField.DATE_WINDOW: "When the case should happen (for example 'week of 11/2' or 'next two weeks').",
    BookingField.PATIENT_NAME: "The patient's name as written.",
    BookingField.PATIENT_DOB: "The patient's date of birth.",
    BookingField.DIAGNOSIS: "The diagnosis or indication (for example 'OA right knee').",
    BookingField.ANESTHESIA_TYPE: "Planned anesthesia (for example general, general with nerve block, MAC).",
    BookingField.PATIENT_CLASS: "Outpatient, extended recovery (overnight) or inpatient.",
    BookingField.IMPLANTS: "Implants, loaner sets and whether a vendor representative attends.",
    BookingField.AUTHORIZATION: "Prior authorization status and number, if stated.",
    BookingField.PREFERENCES: "Days, times or rooms to prefer or avoid.",
    BookingField.CASE_NUMBER: "An existing case number this message refers to.",
    BookingField.CONTACT: "Who sent the request and how to reach them (office, phone, fax).",
}


class Ownership(StrEnum):
    """Whose time a slot is, from the requesting surgeon's point of view."""

    OWN_BLOCK = "own_block"  # the requesting surgeon's block; counts toward their utilization
    RELEASED = "released"  # another owner's block, released (automatically or early)
    OPEN = "open"  # time no block covers
    HELD_BY_OTHER = "held_by_other"  # another owner's block, not yet released: not bookable


class CaseStatus(StrEnum):
    """FHIR Appointment status vocabulary (the subset the agent uses)."""

    PROPOSED = "proposed"
    PENDING = "pending"
    BOOKED = "booked"
    WAITLIST = "waitlist"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Reference records
# ---------------------------------------------------------------------------


class Contact(Model):
    name: str
    phone: str | None = None
    fax: str | None = None
    email: str | None = None


class Surgeon(Model):
    id: str
    first_name: str
    last_name: str
    service: str
    privileges: list[str]  # procedure ids the surgeon is credentialed for
    office: Contact

    @property
    def display_name(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"


class ImplantSpec(Model):
    system: str
    vendor_id: str
    vendor_name: str
    loaner_set: bool
    rep_attends: bool


class Procedure(Model):
    """One entry in the procedure master. Its attributes decide room, equipment and booking strategy."""

    id: str
    name: str
    cpt: str
    aliases: list[str] = []
    laterality: Literal["required", "none"]
    room_capabilities: list[str]
    shared_assets: list[str] = []  # asset types the case must reserve, e.g. orthopedic_robot
    equipment: list[str] = []  # descriptive, for the card and readiness
    implant: ImplantSpec | None = None
    post_op: PostOpDestination
    prior_auth: PriorAuth
    tandem_eligible: bool = False
    default_minutes: int


class Patient(Model):
    mrn: str
    first_name: str
    last_name: str
    dob: date
    sex: Literal["F", "M", "X"]
    payer_id: str | None = None
    h_and_p_date: date | None = None

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Diagnosis(Model):
    code: str
    description: str


class Authorization(Model):
    status: AuthStatus
    number: str | None = None
    valid_through: date | None = None


class SurgicalOrder(Model):
    """The surgeon's order: the source of truth for procedure and side."""

    id: str
    patient_mrn: str
    surgeon_id: str
    procedure_id: str
    laterality: Laterality | None = None
    diagnosis: Diagnosis
    authorization: Authorization
    ordered_on: date


class DecisionClock(Model):
    standard_days: int
    expedited_hours: int


class Payer(Model):
    id: str
    name: str
    kind: Literal["medicare", "medicare_advantage", "commercial", "medicaid"]
    prior_auth: PriorAuth  # for elective surgery
    decision_clock: DecisionClock | None = None


# ---------------------------------------------------------------------------
# The scheduling contract: the agent's two requests and what comes back
# ---------------------------------------------------------------------------


class CaseMinutes(Model):
    typical: int  # P50 in-room minutes
    long: int  # P80 in-room minutes

    @model_validator(mode="after")
    def _ordered(self) -> CaseMinutes:
        if not 0 < self.typical <= self.long:
            raise ValueError("case minutes must satisfy 0 < typical <= long")
        return self


class DateWindow(Model):
    start: date
    end: date

    @model_validator(mode="after")
    def _ordered(self) -> DateWindow:
        if self.end < self.start:
            raise ValueError("date window ends before it starts")
        return self

    def days(self) -> list[date]:
        return [self.start + timedelta(days=i) for i in range((self.end - self.start).days + 1)]


class SearchPreferences(Model):
    avoid_weekdays: list[Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]] = []
    preferred_room_ids: list[str] = []


class AvailabilityQuery(Model):
    """The four facts that find time. Nothing else changes which slots exist."""

    surgeon_id: str
    procedure_id: str
    case_minutes: CaseMinutes
    window: DateWindow
    preferences: SearchPreferences = SearchPreferences()


class SlotOption(Model):
    """One window the scheduling service reports. Received from the service, never computed by the agent.

    `start`..`end` is the free window; a case fits when its length plus the room's
    turnover fits inside it.
    """

    option_id: str
    room_id: str
    start: datetime
    end: datetime
    turnover_minutes: int
    ownership: Ownership
    block_owner_id: str | None = None
    block_owner_name: str | None = None
    released_at: datetime | None = None  # when the block time was released, if it was
    releases_at: datetime | None = None  # when a held block will release, if it will

    @property
    def date(self) -> date:
        return self.start.date()

    @property
    def bookable(self) -> bool:
        return self.ownership is not Ownership.HELD_BY_OTHER

    @property
    def window_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    @property
    def case_capacity_minutes(self) -> int:
        """The longest case that fits, once the room's turnover is set aside."""
        return self.window_minutes - self.turnover_minutes


class AvailabilityResult(Model):
    query: AvailabilityQuery
    options: list[SlotOption]  # bookable now
    held: list[SlotOption]  # would fit, but in another owner's unreleased block
    closed_dates: list[date] = []  # in the window, but the schedule has closed (add-ons)


class Hold(Model):
    hold_id: str
    option_id: str
    request_id: str
    room_id: str
    start: datetime
    end: datetime  # end of the reserved case time, before turnover
    expires_at: datetime


class ImplantRequest(Model):
    system: str
    vendor_id: str
    loaner_set: bool
    rep_attending: bool


class AuthorizationRef(Model):
    status: AuthStatus
    number: str | None = None


class BookingRequest(Model):
    """The chosen option plus the case details the hospital requires. Sent at commit, against a hold."""

    option_id: str
    surgeon_id: str
    procedure_id: str
    patient_mrn: str
    laterality: Laterality | None = None
    diagnosis_code: str
    scheduled_minutes: int
    anesthesia_type: AnesthesiaType
    patient_class: PatientClass
    implants: list[ImplantRequest] = []
    authorization: AuthorizationRef | None = None
    requested_by: Contact | None = None
    booked_by: str
    idempotency_key: str


class BookedCase(Model):
    case_id: str
    status: CaseStatus
    surgeon_id: str
    procedure_id: str
    room_id: str
    start: datetime
    end: datetime
    patient_mrn: str | None = None
    laterality: Laterality | None = None
    diagnosis_code: str | None = None
    anesthesia_type: AnesthesiaType | None = None
    patient_class: PatientClass | None = None
    implants: list[ImplantRequest] = []
    assets: list[str] = []  # shared assets reserved, e.g. ORTHO-ROBOT-1
    requested_by: Contact | None = None
    booked_by: str | None = None
    idempotency_key: str | None = None
    cancel_reason: str | None = None

    @property
    def date(self) -> date:
        return self.start.date()


# ---------------------------------------------------------------------------
# Readiness: what a booking hands downstream
# ---------------------------------------------------------------------------


class ReadinessStatus(StrEnum):
    DONE = "done"
    OPEN = "open"
    AT_RISK = "at_risk"
    OVERDUE = "overdue"


class ReadinessItem(Model):
    rule_id: str  # the hospital readiness rule that created the item
    item: str
    owner: str
    due: datetime | None = None
    status: ReadinessStatus
    depends_on: list[str] = []
    detail: str = ""
