"""The conversation states (Section 6.1). Each request or re-booking task is one instance of the machine."""

from __future__ import annotations

from enum import StrEnum


class State(StrEnum):
    START = "[*]"  # entry point, not a state a request rests in
    INTAKE = "Intake"
    MATCHING = "Matching"
    EVENT_RECEIVED = "EventReceived"
    CASE_LOADED = "CaseLoaded"
    COLLECTING = "Collecting"
    CLARIFYING = "Clarifying"
    AWAITING_REPLY = "AwaitingReply"
    SEARCHING = "Searching"
    PRESENTING = "Presenting"
    HOLDING = "Holding"
    COMPLETING = "Completing"
    CONFIRMING = "Confirming"
    COMMITTING = "Committing"
    BOOKED = "Booked"
    CANCELLING = "Cancelling"
    CANCELLED = "Cancelled"
    ANSWERED = "Answered"
    WAITLISTED = "Waitlisted"
    ROUTED_OUT = "RoutedOut"
    HANDED_OFF = "HandedOff"


# States that wait for input. Clarifying waits only when someone is in the chat to answer.
WAITING = frozenset({State.CLARIFYING, State.AWAITING_REPLY, State.PRESENTING, State.CONFIRMING, State.CANCELLING})

# A request in one of these is finished.
TERMINAL = frozenset({State.BOOKED, State.CANCELLED, State.ANSWERED, State.WAITLISTED, State.ROUTED_OUT, State.HANDED_OFF})
