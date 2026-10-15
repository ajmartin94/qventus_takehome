"""The transition table: the single source for the conversation model.

The orchestrator moves a request only along these edges; anything else is a programming
error. `to_mermaid()` renders the table as the state diagram in
docs/diagrams/booking_flow.md, and a test fails if the two drift apart.

Flow guarantee 1 is visible here: the only edge into `Committing` comes from
`Confirming`.
"""

from __future__ import annotations

from dataclasses import dataclass

from or_booking.orchestrator.states import State

S = State


@dataclass(frozen=True)
class Transition:
    source: State
    target: State
    label: str


TRANSITIONS: tuple[Transition, ...] = tuple(
    Transition(source, target, label)
    for source, target, label in [
        (S.START, S.INTAKE, "request from a person"),
        (S.START, S.EVENT_RECEIVED, "system event"),
        (S.INTAKE, S.MATCHING, "parsed"),
        (S.MATCHING, S.COLLECTING, "new case or reply"),
        (S.MATCHING, S.CASE_LOADED, "modify or reschedule"),
        (S.MATCHING, S.CANCELLING, "cancel"),
        (S.MATCHING, S.ANSWERED, "status or availability"),
        (S.MATCHING, S.ROUTED_OUT, "routed by policy"),
        (S.EVENT_RECEIVED, S.CASE_LOADED, "case displaced"),
        (S.EVENT_RECEIVED, S.PRESENTING, "time opened"),
        (S.CASE_LOADED, S.COLLECTING, "needs a new slot"),
        (S.CASE_LOADED, S.COMPLETING, "keeps its slot"),
        (S.COLLECTING, S.CLARIFYING, "query gap"),
        (S.COLLECTING, S.SEARCHING, "query ready"),
        (S.COLLECTING, S.HANDED_OFF, "hard rule fails"),
        (S.CLARIFYING, S.COLLECTING, "query field answered"),
        (S.CLARIFYING, S.COMPLETING, "booking field answered"),
        (S.CLARIFYING, S.AWAITING_REPLY, "asked by fax or email"),
        (S.CLARIFYING, S.HANDED_OFF, "3 failed attempts"),
        (S.AWAITING_REPLY, S.COLLECTING, "reply arrives"),
        (S.AWAITING_REPLY, S.HANDED_OFF, "no reply by deadline"),
        (S.SEARCHING, S.PRESENTING, "options found"),
        (S.SEARCHING, S.WAITLISTED, "no valid option"),
        (S.SEARCHING, S.ROUTED_OUT, "unsupported strategy"),
        (S.PRESENTING, S.HOLDING, "option selected"),
        (S.PRESENTING, S.WAITLISTED, "other owner's block"),
        (S.HOLDING, S.COMPLETING, "slot held"),
        (S.HOLDING, S.SEARCHING, "slot taken"),
        (S.COMPLETING, S.CLARIFYING, "booking gap"),
        (S.COMPLETING, S.CONFIRMING, "booking request ready"),
        (S.CONFIRMING, S.COMPLETING, "correction"),
        (S.CONFIRMING, S.COMMITTING, "confirmed"),
        (S.COMMITTING, S.BOOKED, "committed"),
        (S.COMMITTING, S.HOLDING, "hold expired"),
        (S.CANCELLING, S.CANCELLED, "confirmed"),
    ]
)

_BY_EDGE = {(t.source, t.target): t for t in TRANSITIONS}


class IllegalTransition(RuntimeError):
    pass


def transition(source: State, target: State) -> Transition:
    try:
        return _BY_EDGE[(source, target)]
    except KeyError:
        raise IllegalTransition(f"{source} -> {target} is not in the transition table") from None


# The diagram's styling, kept with the table so the exported diagram matches the document.
_STYLE = """
    classDef human fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef done fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef waiting fill:#f8fafc,stroke:#94a3b8,color:#475569
    class RoutedOut, HandedOff human
    class Booked, Cancelled, Answered done
    class AwaitingReply, Waitlisted waiting"""


def to_mermaid() -> str:
    lines = ["stateDiagram-v2", "    direction TB"]
    lines += [f"    {t.source} --> {t.target}: {t.label}" for t in TRANSITIONS]
    return "\n".join(lines) + "\n\n" + _STYLE.strip("\n")
