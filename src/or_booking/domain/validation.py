"""Qualifying a request: from proposed values to the two requests the scheduling service accepts.

Section 5.4 of the implementation plan. The agent turns a request carrying dozens of
data points into:

1. an availability query: surgeon, procedure and date window resolved (case length
   comes from sizing), and
2. a booking request: the chosen option plus the hospital's required booking data,
   resolved through lookups, the surgeon's order and validation.

Every function here is pure. Lookups happen in the orchestrator, through ports, and
their results come in as arguments. Values become `resolved` only here; the request
builders refuse anything that isn't.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta

from or_booking.domain.models import (
    AnesthesiaType,
    AuthorizationRef,
    BookingField,
    BookingRequest,
    CaseDraft,
    Contact,
    DateWindow,
    FieldValue,
    ImplantRequest,
    Issue,
    IssueKind,
    Laterality,
    Model,
    Patient,
    PatientClass,
    Payer,
    Procedure,
    ResolvedBy,
    SourceKind,
    Stage,
    Surgeon,
    SurgicalOrder,
)
from or_booking.domain.policy import HospitalPolicies, applicable_requirements, case_facts
from or_booking.domain.readiness import booking_gates

F = BookingField


class Qualification(Model):
    draft: CaseDraft
    issues: list[Issue] = []

    @property
    def ready(self) -> bool:
        return not self.issues


# ---------------------------------------------------------------------------
# Reading values: deterministic normalization of what people write
# ---------------------------------------------------------------------------


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower().replace("b/l", "bilateral"))


def parse_laterality(text: str) -> Laterality | None:
    """'R', 'rt', 'right knee' -> right. Both sides named, or neither, -> None (ask; never guess)."""
    words = set(_words(text))
    found = {
        side
        for side, spellings in (
            (Laterality.RIGHT, {"right", "r", "rt"}),
            (Laterality.LEFT, {"left", "l", "lt"}),
            (Laterality.BILATERAL, {"bilateral", "bilat", "both"}),
        )
        if words & spellings
    }
    return found.pop() if len(found) == 1 else None


def parse_anesthesia(text: str) -> AnesthesiaType | None:
    if text in AnesthesiaType._value2member_map_:
        return AnesthesiaType(text)
    words = set(_words(text))
    general = bool(words & {"general", "ga", "geta"})
    if general and words & {"block", "nerve", "regional"}:
        return AnesthesiaType.GENERAL_WITH_NERVE_BLOCK
    if general:
        return AnesthesiaType.GENERAL
    if words & {"spinal", "epidural", "regional", "block"}:
        return AnesthesiaType.REGIONAL
    if words & {"mac", "sedation"}:
        return AnesthesiaType.MAC
    if "local" in words:
        return AnesthesiaType.LOCAL
    return None


def parse_patient_class(text: str) -> PatientClass | None:
    if text in PatientClass._value2member_map_:
        return PatientClass(text)
    words = set(_words(text))
    if words & {"extended", "overnight", "observation", "obs", "23"}:
        return PatientClass.EXTENDED_RECOVERY
    if words & {"inpatient", "ip", "admit", "admission"}:
        return PatientClass.INPATIENT
    if words & {"outpatient", "op", "ambulatory", "same"}:
        return PatientClass.OUTPATIENT
    return None


def parse_date(text: str, *, today: date, past: bool = False) -> date | None:
    """ISO, M/D/YYYY, M/D/YY or 'March 12, 1958'. Two-digit years land in the past when `past`."""
    text = text.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    if m := re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2})", text):
        month, day, yy = (int(g) for g in m.groups())
        try:
            parsed = date(2000 + yy, month, day)
        except ValueError:
            return None
        return parsed.replace(year=parsed.year - 100) if past and parsed > today else parsed
    return None


def _month_day(text: str, today: date) -> date | None:
    """'11/2' -> the next Nov 2 on or after today; 'M/D/YYYY' and ISO are taken as written."""
    if full := parse_date(text, today=today):
        return full
    if m := re.fullmatch(r"(\d{1,2})/(\d{1,2})", text.strip()):
        month, day = (int(g) for g in m.groups())
        try:
            candidate = date(today.year, month, day)
        except ValueError:
            return None
        return candidate if candidate >= today else candidate.replace(year=today.year + 1)
    return None


_DATE = r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}(?:/\d{2,4})?"


def parse_date_window(text: str, today: date) -> DateWindow | None:
    """'week of 11/2', '2026-11-02/2026-11-06', '11/2 - 11/6', or a single date."""
    lowered = text.lower()
    if m := re.search(rf"week of\s+({_DATE})", lowered):
        anchor = _month_day(m.group(1), today)
        if anchor is None:
            return None
        monday = anchor - timedelta(days=anchor.weekday())
        return DateWindow(start=monday, end=monday + timedelta(days=4))
    if m := re.search(rf"({_DATE})\s*(?:/|\.\.|to|through|thru|–|—|\s-\s|-(?=\d{{1,2}}/))\s*({_DATE})", lowered):
        start, end = _month_day(m.group(1), today), _month_day(m.group(2), today)
        return DateWindow(start=start, end=end) if start and end and end >= start else None
    if m := re.fullmatch(rf"\s*({_DATE})\s*", lowered):
        day = _month_day(m.group(1), today)
        return DateWindow(start=day, end=day) if day else None
    return None


def window_value(window: DateWindow) -> str:
    return f"{window.start.isoformat()}/{window.end.isoformat()}"


def window_from_value(value: str) -> DateWindow:
    start, end = value.split("/")
    return DateWindow(start=date.fromisoformat(start), end=date.fromisoformat(end))


# ---------------------------------------------------------------------------
# Stage 1: what the availability query needs
# ---------------------------------------------------------------------------


def qualify_query(
    draft: CaseDraft, *, surgeons: list[Surgeon], procedures: list[Procedure], today: date
) -> Qualification:
    """`surgeons` and `procedures` are the directory's matches for the stated words."""
    issues: list[Issue] = []
    draft, issue = _resolve_reference(draft, F.SURGEON, [s.id for s in surgeons], "surgeon")
    issues += [issue] if issue else []
    draft, issue = _resolve_reference(draft, F.PROCEDURE, [p.id for p in procedures], "procedure")
    issues += [issue] if issue else []

    surgeon_id, procedure_id = draft.resolved(F.SURGEON), draft.resolved(F.PROCEDURE)
    surgeon = next((s for s in surgeons if s.id == surgeon_id), None)
    if surgeon and procedure_id and procedure_id not in surgeon.privileges:
        issues.append(
            Issue(
                field=F.PROCEDURE,
                kind=IssueKind.NOT_PRIVILEGED,
                stage=Stage.QUERY,
                detail=f"{surgeon.display_name} is not privileged for {procedure_id}",
            )
        )

    fv = draft.get(F.DATE_WINDOW)
    if fv is None:
        issues.append(Issue(field=F.DATE_WINDOW, kind=IssueKind.MISSING, stage=Stage.QUERY, detail="No dates given"))
    elif not fv.is_resolved:
        window = parse_date_window(fv.value, today)
        if window is None:
            issues.append(_issue(F.DATE_WINDOW, IssueKind.INVALID, Stage.QUERY, f"Couldn't read dates from '{fv.stated}'"))
        elif window.end <= today:
            issues.append(_issue(F.DATE_WINDOW, IssueKind.INVALID, Stage.QUERY, f"'{fv.stated}' is in the past"))
        else:
            draft = draft.set(F.DATE_WINDOW, fv.resolve(window_value(window), ResolvedBy.VALIDATION))
    return Qualification(draft=draft, issues=issues)


class QueryInputs(Model):
    surgeon_id: str
    procedure_id: str
    window: DateWindow


def query_inputs(draft: CaseDraft) -> QueryInputs:
    """The resolved inputs a booking strategy turns into an availability query."""
    missing = [f.value for f in (F.SURGEON, F.PROCEDURE, F.DATE_WINDOW) if draft.resolved(f) is None]
    if missing:
        raise ValueError(f"availability query needs resolved {missing}; qualify the draft first")
    return QueryInputs(
        surgeon_id=draft.resolved(F.SURGEON),
        procedure_id=draft.resolved(F.PROCEDURE),
        window=window_from_value(draft.resolved(F.DATE_WINDOW)),
    )


# ---------------------------------------------------------------------------
# Stage 2: what the booking request needs
# ---------------------------------------------------------------------------


def patient_lookup_keys(draft: CaseDraft, today: date) -> tuple[str | None, date | None]:
    """What the orchestrator searches the directory with: the stated name, and the DOB if readable."""
    name, dob = draft.get(F.PATIENT_NAME), draft.get(F.PATIENT_DOB)
    return (name.stated if name else None, _dob(dob, today) if dob else None)


def _dob(fv: FieldValue, today: date) -> date | None:
    return date.fromisoformat(fv.value) if fv.is_resolved else parse_date(fv.value, today=today, past=True)


def resolve_patient(draft: CaseDraft, candidates: list[Patient], today: date) -> Qualification:
    """`candidates` are the directory's matches for `patient_lookup_keys`.

    One match resolves the patient (name -> MRN, and the DOB if given). Whether a date
    of birth is required even with one match is the hospital's booking policy, checked
    in `qualify_booking`, not decided here.
    """
    name, dob = draft.get(F.PATIENT_NAME), draft.get(F.PATIENT_DOB)
    if name is None:
        return Qualification(draft=draft, issues=[_issue(F.PATIENT_NAME, IssueKind.MISSING, Stage.BOOKING, "No patient named")])
    parsed_dob = None
    if dob is not None:
        parsed_dob = _dob(dob, today)
        if parsed_dob is None:
            return Qualification(
                draft=draft, issues=[_issue(F.PATIENT_DOB, IssueKind.INVALID, Stage.BOOKING, f"Couldn't read a date from '{dob.stated}'")]
            )
    if not candidates:
        detail = f"No patient matches '{name.stated}'" + (" with that date of birth" if parsed_dob else "")
        return Qualification(draft=draft, issues=[_issue(F.PATIENT_NAME, IssueKind.NOT_FOUND, Stage.BOOKING, detail)])
    if len(candidates) > 1:
        field = F.PATIENT_NAME if parsed_dob else F.PATIENT_DOB
        detail = f"{len(candidates)} patients match '{name.stated}'" + ("" if parsed_dob else "; a date of birth tells them apart")
        return Qualification(
            draft=draft,
            issues=[_issue(field, IssueKind.AMBIGUOUS, Stage.BOOKING, detail, candidate_count=len(candidates))],
        )
    (patient,) = candidates
    if parsed_dob is not None and parsed_dob != patient.dob:  # a lookup that ignored the DOB; never trust it
        return Qualification(draft=draft, issues=[_issue(F.PATIENT_DOB, IssueKind.NOT_FOUND, Stage.BOOKING, "Date of birth doesn't match")])
    draft = draft.set(F.PATIENT_NAME, name.resolve(patient.mrn, ResolvedBy.LOOKUP, ref=patient.mrn))
    if dob is not None:
        draft = draft.set(F.PATIENT_DOB, dob.resolve(patient.dob.isoformat(), ResolvedBy.LOOKUP, ref=patient.mrn))
    return Qualification(draft=draft)


def matching_order(orders: list[SurgicalOrder], surgeon_id: str, procedure_id: str) -> SurgicalOrder | None:
    return next((o for o in orders if o.surgeon_id == surgeon_id and o.procedure_id == procedure_id), None)


def qualify_booking(
    draft: CaseDraft,
    *,
    procedure: Procedure,
    patient: Patient | None,
    orders: list[SurgicalOrder],
    payer: Payer | None,
    policies: HospitalPolicies,
    surgery_date: date | None,
    today: date,
) -> Qualification:
    """Check the booking request against the surgeon's order and the hospital's booking policy.

    `orders` are the resolved patient's surgical orders. Runs after `resolve_patient`.
    """
    issues: list[Issue] = []
    surgeon_id = draft.resolved(F.SURGEON) or ""
    order = matching_order(orders, surgeon_id, procedure.id)
    other_order = next((o for o in orders if o.surgeon_id == surgeon_id), None) if order is None else None
    facts = case_facts(
        procedure=procedure,
        payer=payer,
        authorization=order.authorization if order else None,
        patient=patient,
        loaner_first_time=draft.loaner_first_time,
        urgency=draft.stated_urgency,
    )
    requirements = applicable_requirements(policies, facts)

    if other_order is not None:
        issues.append(
            _issue(
                F.PROCEDURE,
                IssueKind.CONFLICTS_WITH_ORDER,
                Stage.BOOKING,
                f"Request is for {procedure.id}; the surgeon's order {other_order.id} is for {other_order.procedure_id}",
            )
        )
    elif order is None and patient is not None:
        issues.append(
            _issue(F.DIAGNOSIS, IssueKind.NOT_FOUND, Stage.BOOKING, "No surgical order on file for this patient, surgeon and procedure")
        )

    # Side: spelled out, and the same as the surgeon's order when the hospital requires it
    must_match = any(r.must_match_order and F.LATERALITY in r.require for r in requirements)
    side = draft.get(F.LATERALITY)
    if side is not None and not side.is_resolved and procedure.laterality == "required":
        parsed = parse_laterality(side.value)
        if parsed is None:
            issues.append(_issue(F.LATERALITY, IssueKind.INVALID, Stage.BOOKING, f"Can't tell the side from '{side.stated}'"))
        elif must_match and order is not None and order.laterality != parsed:
            issues.append(
                _issue(
                    F.LATERALITY,
                    IssueKind.CONFLICTS_WITH_ORDER,
                    Stage.BOOKING,
                    f"Request says {parsed.value}; the surgeon's order {order.id} says {order.laterality.value if order.laterality else 'no side'}",
                )
            )
        elif order is not None and order.laterality == parsed:
            draft = draft.set(F.LATERALITY, side.resolve(parsed.value, ResolvedBy.SURGEONS_ORDER, ref=order.id))
        else:
            draft = draft.set(F.LATERALITY, side.resolve(parsed.value, ResolvedBy.VALIDATION))

    # Diagnosis code comes from the surgeon's order; the stated words stay as evidence
    if order is not None and draft.resolved(F.DIAGNOSIS) is None:
        stated = draft.get(F.DIAGNOSIS) or FieldValue.proposed(
            order.diagnosis.description, SourceKind.SURGEONS_ORDER, evidence=order.diagnosis.description
        )
        draft = draft.set(F.DIAGNOSIS, stated.resolve(order.diagnosis.code, ResolvedBy.SURGEONS_ORDER, ref=order.id))

    for field, parse in ((F.ANESTHESIA_TYPE, parse_anesthesia), (F.PATIENT_CLASS, parse_patient_class)):
        fv = draft.get(field)
        if fv is not None and not fv.is_resolved:
            parsed_value = parse(fv.value)
            if parsed_value is None:
                issues.append(_issue(field, IssueKind.INVALID, Stage.BOOKING, f"Couldn't read '{fv.stated}' as {field.value}"))
            else:
                draft = draft.set(field, fv.resolve(parsed_value.value, ResolvedBy.VALIDATION))

    implants = draft.get(F.IMPLANTS)
    if implants is not None and not implants.is_resolved and procedure.implant is not None:
        draft = draft.set(F.IMPLANTS, implants.resolve(procedure.implant.vendor_id, ResolvedBy.LOOKUP, ref=procedure.id))

    # The hospital's required booking data
    raised = {i.field for i in issues}
    for requirement in requirements:
        for field in requirement.require:
            if field in raised or draft.resolved(field) is not None:
                continue
            fv = draft.get(field)
            kind, detail = (IssueKind.MISSING, requirement.description) if fv is None else (
                IssueKind.INVALID,
                f"'{fv.stated}' couldn't be checked",
            )
            issues.append(_issue(field, kind, Stage.BOOKING, detail, rule_id=requirement.id))
            raised.add(field)

    # Readiness rules that gate booking itself
    if surgery_date is not None:
        for gate in booking_gates(policies, facts, surgery_date, today):
            if gate.blocks_booking:
                rule = next(r for r in policies.readiness if r.id == gate.rule_id)
                issues.append(
                    _issue(
                        rule.gates_booking.asks_for,
                        IssueKind.GATED,
                        Stage.BOOKING,
                        f"Surgery is {gate.days_until_surgery} days out; booking within "
                        f"{gate.within_days_of_surgery} days requires: {rule.item.lower()}",
                        rule_id=gate.rule_id,
                    )
                )
    return Qualification(draft=draft, issues=issues)


# ---------------------------------------------------------------------------
# Which question next, and the booking request itself
# ---------------------------------------------------------------------------

_FIELD_ORDER = [
    F.SURGEON, F.PROCEDURE, F.DATE_WINDOW,
    F.PATIENT_NAME, F.PATIENT_DOB, F.LATERALITY, F.DIAGNOSIS,
    F.ANESTHESIA_TYPE, F.PATIENT_CLASS, F.IMPLANTS, F.AUTHORIZATION,
    F.CONTACT, F.PREFERENCES, F.CASE_NUMBER,
]  # fmt: skip


def next_issue(issues: list[Issue]) -> Issue | None:
    """The single most blocking issue: query gaps before booking gaps, hard failures first, then field order."""
    stage_order = {Stage.QUERY: 0, Stage.BOOKING: 1}
    return min(issues, key=lambda i: (stage_order[i.stage], not i.hard, _FIELD_ORDER.index(i.field)), default=None)


def build_booking_request(
    draft: CaseDraft,
    *,
    option_id: str,
    procedure: Procedure,
    scheduled_minutes: int,
    booked_by: str,
    idempotency_key: str,
    requested_by: Contact | None = None,
    authorization: AuthorizationRef | None = None,
) -> BookingRequest:
    """Built only from resolved values. `authorization` is passed only when a booking gate applies."""
    needed = [F.SURGEON, F.PROCEDURE, F.PATIENT_NAME, F.DIAGNOSIS, F.ANESTHESIA_TYPE, F.PATIENT_CLASS]
    if procedure.laterality == "required":
        needed.append(F.LATERALITY)
    if procedure.implant is not None:
        needed.append(F.IMPLANTS)
    unresolved = [f.value for f in needed if draft.resolved(f) is None]
    if unresolved:
        raise ValueError(f"booking request needs resolved {unresolved}; qualify the draft first")
    if draft.resolved(F.PROCEDURE) != procedure.id:
        raise ValueError("procedure record doesn't match the draft")

    implant = procedure.implant
    side = draft.resolved(F.LATERALITY)
    return BookingRequest(
        option_id=option_id,
        surgeon_id=draft.resolved(F.SURGEON),
        procedure_id=procedure.id,
        patient_mrn=draft.resolved(F.PATIENT_NAME),
        laterality=Laterality(side) if side else None,
        diagnosis_code=draft.resolved(F.DIAGNOSIS),
        scheduled_minutes=scheduled_minutes,
        anesthesia_type=AnesthesiaType(draft.resolved(F.ANESTHESIA_TYPE)),
        patient_class=PatientClass(draft.resolved(F.PATIENT_CLASS)),
        implants=[
            ImplantRequest(
                system=implant.system,
                vendor_id=implant.vendor_id,
                loaner_set=implant.loaner_set,
                rep_attending=implant.rep_attends,
            )
        ]
        if implant
        else [],
        authorization=authorization,
        requested_by=requested_by,
        booked_by=booked_by,
        idempotency_key=idempotency_key,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _issue(field: BookingField, kind: IssueKind, stage: Stage, detail: str, **extra) -> Issue:
    return Issue(field=field, kind=kind, stage=stage, detail=detail, **extra)


def _resolve_reference(draft: CaseDraft, field: BookingField, matches: list[str], noun: str) -> tuple[CaseDraft, Issue | None]:
    fv = draft.get(field)
    if fv is None:
        return draft, _issue(field, IssueKind.MISSING, Stage.QUERY, f"No {noun} named")
    if fv.is_resolved:
        return draft, None
    if not matches:
        return draft, _issue(field, IssueKind.NOT_FOUND, Stage.QUERY, f"No {noun} matches '{fv.stated}'")
    if len(matches) > 1:
        return draft, _issue(
            field, IssueKind.AMBIGUOUS, Stage.QUERY, f"{len(matches)} {noun}s match '{fv.stated}'", candidate_count=len(matches)
        )
    return draft.set(field, fv.resolve(matches[0], ResolvedBy.LOOKUP, ref=matches[0])), None
