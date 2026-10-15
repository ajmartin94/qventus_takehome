"""What the model may return: a closed set of intents and field mentions (Section 6.4).

Structured outputs constrain the model to these shapes. Values are strings as stated
(ISO dates when unambiguous), each with the exact words it came from. There are no
identifiers here: the model never names an MRN or a procedure id; code resolves words.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from or_booking.domain.models import BookingField, Contact


class Intent(StrEnum):
    NEW_REQUEST = "new_request"
    PROVIDE_INFO = "provide_info"
    SELECT_OPTION = "select_option"
    CONFIRM = "confirm"
    CORRECT = "correct"
    ASK_STATUS = "ask_status"
    ASK_AVAILABILITY = "ask_availability"
    REQUEST_WAITLIST = "request_waitlist"
    REQUEST_RELEASE = "request_release"
    MODIFY_CASE = "modify_case"
    CANCEL_CASE = "cancel_case"
    READINESS_UPDATE = "readiness_update"
    URGENT_REQUEST = "urgent_request"
    CLINICAL_QUESTION = "clinical_question"
    TALK_TO_HUMAN = "talk_to_human"
    UNCLEAR = "unclear"


INTENT_DEFINITIONS: dict[Intent, str] = {
    Intent.NEW_REQUEST: "A case to be booked.",
    Intent.PROVIDE_INFO: "Answers a question or adds details to the request being worked.",
    Intent.SELECT_OPTION: "Picks one of the options on screen (give its number in selected_option).",
    Intent.CONFIRM: "Approves the confirmation card as shown.",
    Intent.CORRECT: "Changes something already given (put the new values in corrections).",
    Intent.ASK_STATUS: "Asks whether a case is booked, or what is still open on it.",
    Intent.ASK_AVAILABILITY: "Asks what time is open, with no case to book yet.",
    Intent.REQUEST_WAITLIST: "Asks to wait for time that isn't available now.",
    Intent.REQUEST_RELEASE: "Wants time in another owner's block, or a day that isn't offered.",
    Intent.MODIFY_CASE: "Wants to change a case that is already booked.",
    Intent.CANCEL_CASE: "Wants to cancel a booked case.",
    Intent.READINESS_UPDATE: "Reports progress on a booked case: authorization approved, H&P uploaded, tray confirmed.",
    Intent.URGENT_REQUEST: "Says the case is urgent or emergent, or needs a room today or tonight.",
    Intent.CLINICAL_QUESTION: "Asks a clinical question, such as fitness for surgery or anesthesia.",
    Intent.TALK_TO_HUMAN: "Asks for a person.",
    Intent.UNCLEAR: "None of the above, or can't tell.",
}


class _Schema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Mention(_Schema):
    field: BookingField = Field(description="Which booking field the words give a value for")
    value: str = Field(description="The value as stated; ISO dates (YYYY-MM-DD, or start/end for ranges) when unambiguous")
    evidence: str = Field(description="The exact words it came from, copied verbatim")


class TurnInterpretation(_Schema):
    """One coordinator message, read in the context of the request being worked."""

    intent: Intent
    mentions: list[Mention] = []
    selected_option: int | None = Field(default=None, description="1-based number of the option picked, from the options on screen")
    corrections: list[Mention] = []
    stated_urgency: Literal["none", "urgent", "emergent"] = "none"
    cancel_reason: str | None = None
    unclear: list[str] = Field(default=[], description="Anything that couldn't be interpreted")


class ExtractedRequest(_Schema):
    """An inbound fax, email or call transcript, read as a request."""

    channel: Literal["fax", "email", "call_transcript", "portal"]
    intent: Intent
    mentions: list[Mention] = Field(default=[], description="Every booking field found; evidence is a verbatim snippet")
    sender: Contact | None = None
    stated_urgency: Literal["none", "urgent", "emergent"] = "none"
    unreadable: list[str] = Field(default=[], description="Parts of the document that couldn't be read")


class OptionLine(_Schema):
    number: int
    summary: str


class TurnContext(_Schema):
    """The current state in brief, as the interpretation prompt shows it."""

    today: str = ""  # ISO date, so "Tuesday" or "11/9" can be normalized to a full date
    state: str
    filled: dict[str, str] = {}
    open_question: str | None = None
    options: list[OptionLine] = []
