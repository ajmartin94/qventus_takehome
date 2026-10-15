"""Matching an incoming request to open drafts and booked cases (Section 5.9).

- A case number matches a booked case directly.
- Otherwise the request is matched on patient, surgeon and procedure. A match with an
  open draft is a continuation (it adds something) or a duplicate (nothing new). A
  match with a booked case is a request about that case: status, modify or cancel.
- An ambiguous match goes to the coordinator, never to a guess.

Fields are compared by their resolved values when both sides have them, and otherwise
by the words as stated (one side's words contained in the other's, ignoring titles and
side words), so a late fax that names the patient matches the draft still waiting on
that patient's date of birth.
"""

from __future__ import annotations

import re
from enum import StrEnum

from or_booking.domain.models import BookedCase, BookingField, CaseDraft, CaseStatus, Model

F = BookingField
_IGNORED = {"dr", "doctor", "md", "r", "l", "rt", "lt", "right", "left", "the", "of", "for"}


class MatchKind(StrEnum):
    NEW = "new"
    CONTINUATION = "continuation"
    DUPLICATE = "duplicate"
    BOOKED_CASE = "booked_case"
    AMBIGUOUS = "ambiguous"


class MatchResult(Model):
    kind: MatchKind
    request_id: str | None = None  # the open draft it continues or duplicates
    case_id: str | None = None  # the booked case it's about
    candidates: list[str] = []  # draft or case ids, when ambiguous
    reason: str


def match_request(incoming: CaseDraft, open_drafts: list[CaseDraft], booked: list[BookedCase]) -> MatchResult:
    case_number = incoming.get(F.CASE_NUMBER)
    if case_number is not None:
        wanted = case_number.value.strip().upper()
        case = next((c for c in booked if c.case_id.upper() == wanted), None)
        if case is not None:
            return MatchResult(kind=MatchKind.BOOKED_CASE, case_id=case.case_id, reason=f"Case number {case.case_id}")
        return MatchResult(kind=MatchKind.AMBIGUOUS, reason=f"No booked case numbered {case_number.stated}")

    mrn = incoming.resolved(F.PATIENT_NAME)
    if mrn is not None:
        cases = [
            c
            for c in booked
            if c.status is CaseStatus.BOOKED
            and c.patient_mrn == mrn
            and _compatible_id(incoming, F.SURGEON, c.surgeon_id)
            and _compatible_id(incoming, F.PROCEDURE, c.procedure_id)
        ]
        if len(cases) == 1:
            return MatchResult(kind=MatchKind.BOOKED_CASE, case_id=cases[0].case_id, reason="Same patient, surgeon and procedure")
        if len(cases) > 1:
            return MatchResult(
                kind=MatchKind.AMBIGUOUS, candidates=[c.case_id for c in cases], reason="Several booked cases for this patient"
            )

    drafts = [
        d
        for d in open_drafts
        if d.request_id != incoming.request_id
        and _same_patient(incoming, d)
        and all(_compatible(incoming, d, f) for f in (F.SURGEON, F.PROCEDURE))
    ]
    if not drafts:
        return MatchResult(kind=MatchKind.NEW, reason="No open draft or booked case matches")
    if len(drafts) > 1:
        return MatchResult(
            kind=MatchKind.AMBIGUOUS, candidates=[d.request_id for d in drafts], reason="Several open drafts for this patient"
        )
    (draft,) = drafts
    adds = [f.value for f, fv in incoming.fields.items() if not _same_value(fv, draft.get(f))]
    if adds:
        return MatchResult(kind=MatchKind.CONTINUATION, request_id=draft.request_id, reason=f"Adds {', '.join(adds)}")
    return MatchResult(kind=MatchKind.DUPLICATE, request_id=draft.request_id, reason="Nothing new")


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - _IGNORED


def _same_value(a, b) -> bool:
    if b is None:
        return False
    if a.is_resolved and b.is_resolved:
        return a.value == b.value
    return _words(a.stated) == _words(b.stated)


def _compatible(a: CaseDraft, b: CaseDraft, field: BookingField) -> bool:
    """Missing on either side is compatible; otherwise the same id, or one's words within the other's."""
    fa, fb = a.get(field), b.get(field)
    if fa is None or fb is None:
        return True
    if fa.is_resolved and fb.is_resolved:
        return fa.value == fb.value
    wa, wb = _words(fa.stated), _words(fb.stated)
    return bool(wa and wb) and (wa <= wb or wb <= wa)


def _compatible_id(draft: CaseDraft, field: BookingField, record_id: str) -> bool:
    resolved = draft.resolved(field)
    return resolved is None or resolved == record_id


def _same_patient(a: CaseDraft, b: CaseDraft) -> bool:
    if a.get(F.PATIENT_NAME) is None or b.get(F.PATIENT_NAME) is None:
        return False
    dob_a, dob_b = a.get(F.PATIENT_DOB), b.get(F.PATIENT_DOB)
    if dob_a and dob_b and dob_a.is_resolved and dob_b.is_resolved and dob_a.value != dob_b.value:
        return False
    return _compatible(a, b, F.PATIENT_NAME)
