"""Intake routing (diagram 1): match an input to open requests and booked cases, and detect situations.

Code detects a closed set of situations; the hospital's routing policy decides who
handles each. Matching decides whether an input is a new request, a reply to an open
one, a duplicate, or about a booked case. Ambiguity goes to a person, never to a guess.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from or_booking.domain.errors import NotFound
from or_booking.domain.matching import MatchKind, MatchResult, match_request
from or_booking.domain.models import BookedCase, BookingField
from or_booking.domain.policy import Situation
from or_booking.interpretation.schemas import Intent
from or_booking.orchestrator.context import Go, Merge, Step
from or_booking.orchestrator.session import Session, SessionKind
from or_booking.orchestrator.states import State

if TYPE_CHECKING:
    from or_booking.orchestrator.handlers import Handlers

F = BookingField

_SITUATION_BY_INTENT = {
    Intent.URGENT_REQUEST: Situation.URGENT_OR_EMERGENT,
    Intent.CLINICAL_QUESTION: Situation.CLINICAL_QUESTION,
    Intent.TALK_TO_HUMAN: Situation.HUMAN_REQUESTED,
    Intent.READINESS_UPDATE: Situation.READINESS_UPDATE,
}


def situation_for(intent: Intent | None, stated_urgency: str) -> Situation | None:
    if stated_urgency in ("urgent", "emergent"):
        return Situation.URGENT_OR_EMERGENT
    return _SITUATION_BY_INTENT.get(intent) if intent else None


def route_intake(h: Handlers, s: Session) -> Step:
    intent = s.intent or Intent.UNCLEAR
    situation = situation_for(intent, s.draft.stated_urgency)
    if situation is not None and not h.route(s, situation, _situation_reason(situation, s)):
        return Go(State.ROUTED_OUT)

    probe = h.identify_patient(s.draft)
    mrn = probe.resolved(F.PATIENT_NAME)
    open_drafts = [o.draft for o in h.repo.open() if o.request_id != s.request_id]
    booked = h.ports.scheduling.find_cases(patient_mrn=mrn) if mrn else []
    if s.draft.get(F.CASE_NUMBER) is not None:
        booked = [*booked, *_case_by_number(h, s)]
    match = match_request(probe, open_drafts, booked)
    h.decide(s, "matching", match.model_dump(mode="json"))

    if intent is Intent.ASK_STATUS:
        return h.answer_status(s, match)
    if intent is Intent.ASK_AVAILABILITY:
        return h.answer_availability(s)
    if match.kind is MatchKind.AMBIGUOUS:
        h.route(s, Situation.AMBIGUOUS_MATCH, f"{match.reason}: {', '.join(match.candidates) or 'no candidates'}")
        return Go(State.ROUTED_OUT)
    if match.kind is MatchKind.CONTINUATION:
        return Merge(match.request_id or "")
    if match.kind is MatchKind.DUPLICATE:
        return _answered(s, "Duplicate", [("Duplicate of", match.request_id or "")], f"Duplicate of open request {match.request_id}; nothing new to add.")
    if match.kind is MatchKind.BOOKED_CASE:
        return _about_booked_case(s, intent, match)
    if intent in (Intent.CANCEL_CASE, Intent.MODIFY_CASE):
        return _answered(s, "No matching case", [("Reason", match.reason)], "No booked case matches this request.")
    return Go(State.COLLECTING)


def _about_booked_case(s: Session, intent: Intent, match: MatchResult) -> Step:
    s.case_id = match.case_id
    if intent is Intent.CANCEL_CASE:
        s.kind = SessionKind.CANCEL
        return Go(State.CANCELLING)
    if intent is Intent.MODIFY_CASE:
        return Go(State.CASE_LOADED)
    return _answered(s, "Already booked", [("Case", match.case_id or ""), ("Reason", match.reason)], f"Already booked as {match.case_id}.")


def _answered(s: Session, title: str, rows: list[tuple[str, str]], summary: str) -> Step:
    s.kind = SessionKind.INQUIRY
    s.answer, s.summary = [("Answer", title), *rows], summary
    return Go(State.ANSWERED)


def _case_by_number(h: Handlers, s: Session) -> list[BookedCase]:
    number = s.draft.get(F.CASE_NUMBER)
    try:
        return [h.ports.scheduling.get_case(number.value.strip().upper())] if number else []
    except NotFound:  # matching reports an unknown number as ambiguous
        return []


def _situation_reason(situation: Situation, s: Session) -> str:
    return {
        Situation.URGENT_OR_EMERGENT: f"Stated as {s.draft.stated_urgency if s.draft.stated_urgency != 'none' else 'urgent'}",
        Situation.CLINICAL_QUESTION: "Clinical question",
        Situation.HUMAN_REQUESTED: "Asked for a person",
        Situation.READINESS_UPDATE: "Readiness update on a booked case",
    }.get(situation, situation.value)
