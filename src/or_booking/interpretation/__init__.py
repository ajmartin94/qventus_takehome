"""The language-model boundary: interpretation schemas, the versioned prompt registry, and the interpreter.

The model turns messy input into proposed values and turns structured results into
readable replies; it never decides.
"""

from or_booking.interpretation.interpreter import PROMPT_VERSIONS, Interpreter, PromptSettings
from or_booking.interpretation.prompts import PromptRegistry
from or_booking.interpretation.schemas import (
    ExtractedRequest,
    Intent,
    Mention,
    OptionLine,
    TurnContext,
    TurnInterpretation,
)

__all__ = [
    "PROMPT_VERSIONS",
    "ExtractedRequest",
    "Intent",
    "Interpreter",
    "Mention",
    "OptionLine",
    "PromptRegistry",
    "PromptSettings",
    "TurnContext",
    "TurnInterpretation",
]
