"""Drive the real orchestrator with scripted interpretations. Each flow is one path through the machine."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from or_booking.adapters.audit_jsonl import MemoryAuditLog
from or_booking.adapters.clock import FrozenClock
from or_booking.adapters.llm_fake import ScriptedLLM
from or_booking.adapters.store_memory import MemoryStore
from or_booking.app import build, build_orchestrator, load_config
from or_booking.channels.scenario import load_scenario
from or_booking.orchestrator import TurnResult
from or_booking.ports.audit_log import AuditKind
from or_booking.ports.event_source import EventType, ScheduleEvent
from tests.conftest import DEMO_NOW, PROJECT_ROOT

D1 = load_scenario(PROJECT_ROOT / "scenarios" / "demo" / "d1_faxed_request.yaml")


def turn(intent: str, *, option: int | None = None, urgency: str = "none", reason: str | None = None, corrections: dict | None = None, **slots: str) -> dict[str, Any]:
    """A scripted interpretation: turn('select_option', option=1, patient_dob='1958-03-12')."""
    mention = lambda f, v: {"field": f, "value": v, "evidence": v}  # noqa: E731
    return {
        "intent": intent,
        "selected_option": option,
        "mentions": [mention(f, v) for f, v in slots.items()],
        "corrections": [mention(f, v) for f, v in (corrections or {}).items()],
        "stated_urgency": urgency,
        "cancel_reason": reason,
    }


class Harness:
    def __init__(self, now: datetime = DEMO_NOW) -> None:
        self.clock = FrozenClock(now)
        self.audit = MemoryAuditLog()
        self.llm = ScriptedLLM()
        config, root = load_config(PROJECT_ROOT / "config" / "app.yaml")
        self.services = build(
            config, project_root=root, overrides={"clock": self.clock, "audit_log": self.audit, "store": MemoryStore(), "llm": self.llm}
        )
        self.agent = build_orchestrator(self.services)

    def document(self, document_id: str, extraction: dict[str, Any], *, interactive: bool = True) -> TurnResult:
        self.llm.queue("extract_document", extraction)
        return self.agent.receive_document(document_id, interactive=interactive)

    def message(self, text: str, interpretation: dict[str, Any]) -> TurnResult:
        self.llm.queue("interpret_turn", interpretation)
        return self.agent.receive_message(text)

    def reply(self, result: TurnResult, text: str, interpretation: dict[str, Any]) -> TurnResult:
        self.llm.queue("interpret_turn", interpretation)
        return self.agent.reply(result.request_id, text)

    def event(self, kind: EventType, **fields: Any) -> list[TurnResult]:
        self.services.event_source.inject(ScheduleEvent(event_id=f"E-{kind.value}", type=kind, occurred_at=self.clock.now(), **fields))
        return self.agent.process_events()

    def transitions(self) -> set[tuple[str, str]]:
        return {tuple(e.name.split(" -> ")) for e in self.audit.entries() if e.kind is AuditKind.TRANSITION}  # type: ignore[misc]


def names(result: TurnResult) -> list[str]:
    return [s.value for s in result.trace]


# ---------------------------------------------------------------------------
# Flows
# ---------------------------------------------------------------------------

NEW_KNEE = turn("new_request", surgeon="Dr. Patel", procedure="robotic TKA", laterality="right", patient_name="Maria Gomez")


def d1_presenting(h: Harness) -> TurnResult:
    return h.document("fax_001", D1.scripted_extraction or {})


def d1_confirming(h: Harness) -> TurnResult:
    return h.reply(d1_presenting(h), "DOB 3/12/1958, take Tuesday", turn("select_option", option=1, patient_dob="1958-03-12"))


def d1_booked(h: Harness) -> TurnResult:
    return h.reply(d1_confirming(h), "confirm", turn("confirm"))


def query_gap_answered(h: Harness) -> tuple[TurnResult, TurnResult]:
    asked = h.message("Robotic right knee for Maria Gomez with Dr. Patel", NEW_KNEE)
    return asked, h.reply(asked, "week of 11/2", turn("provide_info", date_window="2026-11-02/2026-11-06"))


def booking_gap_answered(h: Harness) -> tuple[TurnResult, TurnResult]:
    asked = h.reply(d1_presenting(h), "take Tuesday", turn("select_option", option=1))
    return asked, h.reply(asked, "3/12/1958", turn("provide_info", patient_dob="1958-03-12"))


def attempts_exhausted(h: Harness) -> TurnResult:
    result = h.message("Robotic right knee for Maria Gomez with Dr. Patel", NEW_KNEE)
    for _ in range(3):
        result = h.reply(result, "not sure yet", turn("provide_info"))
    return result


def hard_rule(h: Harness) -> TurnResult:
    return h.message(
        "Robotic TKA for John Carter with Dr. Chen next week",
        turn("new_request", surgeon="Dr. Chen", procedure="robotic TKA", patient_name="John Carter", date_window="2026-11-02/2026-11-06"),
    )


RAHMAN_EMAIL = {
    "channel": "email",
    "intent": "new_request",
    "mentions": [
        {"field": "surgeon", "value": "Dr. Patel", "evidence": "for Dr. Patel"},
        {"field": "procedure", "value": "L THA", "evidence": "Procedure: L THA"},
        {"field": "laterality", "value": "left", "evidence": "L THA"},
        {"field": "patient_name", "value": "Aisha Rahman", "evidence": "Patient: Aisha Rahman"},
        {"field": "anesthesia_type", "value": "general", "evidence": "Anesthesia: general"},
        {"field": "patient_class", "value": "extended recovery (overnight)", "evidence": "Class: extended recovery (overnight)"},
        {"field": "implants", "value": "hip system, loaner set, rep to attend", "evidence": "Implants: hip system, loaner set, rep to attend"},
    ],
    "unreadable": ["Dates line"],
}
RAHMAN_REPLY = {
    "channel": "fax",
    "intent": "provide_info",
    "mentions": [
        {"field": "patient_name", "value": "Aisha Rahman", "evidence": "Aisha Rahman (Dr. Patel)"},
        {"field": "surgeon", "value": "Dr. Patel", "evidence": "(Dr. Patel)"},
        {"field": "patient_dob", "value": "1949-05-19", "evidence": "Patient DOB is 05/19/1949."},
    ],
}


def unattended_reply(h: Harness) -> tuple[TurnResult, TurnResult]:
    parked = h.document("email_003", RAHMAN_EMAIL, interactive=False)
    h.clock.set(datetime(2026, 10, 14, 13, 30))
    return parked, h.document("fax_004", RAHMAN_REPLY, interactive=False)


def reply_deadline(h: Harness) -> list[TurnResult]:
    unattended_reply(h)
    h.clock.set(datetime(2026, 10, 15, 14, 0))  # one business day after the last question
    return h.agent.tick()


def wednesday_only(h: Harness) -> TurnResult:
    return h.message(
        "Robotic right knee for Maria Gomez with Dr. Patel, Wednesday Nov 4 only",
        turn("new_request", surgeon="Dr. Patel", procedure="robotic TKA", laterality="right", patient_name="Maria Gomez", date_window="2026-11-04"),
    )


def time_opened(h: Harness) -> list[TurnResult]:
    wednesday_only(h)
    h.clock.set(datetime(2026, 10, 21, 7, 0))  # Dr. Ruiz's robotic Wednesday releases
    return h.event(EventType.TIME_OPENED, room_id="OR-6")


def cardiac(h: Harness) -> TurnResult:
    return h.message(
        "CABG for Linda Novak with Dr. Lee, week of 11/2",
        turn("new_request", surgeon="Dr. Lee", procedure="CABG", patient_name="Linda Novak", date_window="2026-11-02/2026-11-06"),
    )


def other_owners_block(h: Harness) -> tuple[TurnResult, TurnResult]:
    asked = h.reply(d1_presenting(h), "Can we do Wednesday instead?", turn("request_release", date_window="2026-11-04"))
    return asked, h.reply(asked, "waitlist it for Wednesday", turn("request_waitlist"))


def slot_taken(h: Harness) -> TurnResult:
    presenting = d1_presenting(h)
    h.services.scheduling.place_hold("OPT-OR5-20261103-1300", "REQ-SOMEONE-ELSE")  # another coordinator, a moment earlier
    return h.reply(presenting, "DOB 3/12/1958, take Tuesday", turn("select_option", option=1, patient_dob="1958-03-12"))


def correction(h: Harness) -> TurnResult:
    return h.reply(d1_confirming(h), "make it general anesthesia", turn("correct", corrections={"anesthesia_type": "general"}))


def hold_expired(h: Harness) -> tuple[TurnResult, TurnResult]:
    confirming = d1_confirming(h)
    h.clock.advance(minutes=11)
    reheld = h.reply(confirming, "confirm", turn("confirm"))
    return reheld, h.reply(reheld, "confirm", turn("confirm"))


def urgent(h: Harness) -> TurnResult:
    return h.message(
        "Dr. Mehta needs a room tonight for James Whitaker, right tibia nail",
        turn("urgent_request", urgency="urgent", surgeon="Dr. Mehta", procedure="tibia nail", laterality="right", patient_name="James Whitaker", date_window="tonight"),
    )


def status_question(h: Harness) -> TurnResult:
    d1_booked(h)
    return h.message("Is the Gomez case on? DOB 3/12/1958", turn("ask_status", patient_name="Maria Gomez", patient_dob="1958-03-12"))


def cancellation(h: Harness) -> tuple[TurnResult, TurnResult]:
    d1_booked(h)
    asked = h.message(
        "Cancel the Gomez case, DOB 3/12/1958; the patient asked to cancel",
        turn("cancel_case", reason="patient asked to cancel", patient_name="Maria Gomez", patient_dob="1958-03-12"),
    )
    return asked, h.reply(asked, "confirm", turn("confirm"))


def modification(h: Harness) -> tuple[TurnResult, TurnResult]:
    d1_booked(h)
    asked = h.message("Change C-5001 to general anesthesia", turn("modify_case", case_number="C-5001", anesthesia_type="general"))
    return asked, h.reply(asked, "confirm", turn("confirm"))


def displaced(h: Harness) -> list[TurnResult]:
    (asked,) = h.event(EventType.CASE_DISPLACED, case_ids=["C-4417"])
    presenting = h.reply(asked, "look at the week of 11/9", turn("provide_info", date_window="2026-11-09/2026-11-13"))
    confirming = h.reply(presenting, "take the first one", turn("select_option", option=1))
    return [asked, presenting, confirming, h.reply(confirming, "confirm", turn("confirm"))]


ALL_FLOWS = [
    d1_booked, query_gap_answered, booking_gap_answered, attempts_exhausted, hard_rule, unattended_reply, reply_deadline,
    wednesday_only, time_opened, cardiac, other_owners_block, slot_taken, correction, hold_expired, urgent,
    status_question, cancellation, modification, displaced,
]  # fmt: skip
