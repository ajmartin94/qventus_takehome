"""LLMClient port: structured interpretation and extraction, and short phrasing.

The model is called through this port at a few fixed points and never decides
anything. Structured output guarantees the shape of a response, not its truth; every
value still goes through lookups and validation. A refusal, a truncated response or a
malformed one comes back as `refused` / `value=None` (or `LLMOutputInvalid`), which
the orchestrator treats as "ask the coordinator", never as a guess.
"""

from __future__ import annotations

from typing import Generic, Literal, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel, ConfigDict

from or_booking.domain.errors import BookingError
from or_booking.domain.models import Model

T = TypeVar("T")


class LLMRequest(Model):
    prompt_id: str  # e.g. "interpret_turn"
    prompt_version: str  # e.g. "v1"; logged with every call
    system: str  # the stable, cache-friendly part comes first
    user: str  # per-request state and the message come last
    model: str | None = None  # None: the adapter's configured default
    effort: Literal["low", "medium", "high", "xhigh", "max"] | None = None
    max_tokens: int | None = None  # None: the adapter's default (thinking counts against it, so don't lowball)


class TokenUsage(Model):
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


class LLMResult(BaseModel, Generic[T]):
    model_config = ConfigDict(frozen=True)

    value: T | None
    text: str = ""
    stop_reason: str | None = None
    refused: bool = False
    model: str | None = None
    usage: TokenUsage = TokenUsage()


class LLMUnavailable(BookingError):
    code = "LLM_UNAVAILABLE"


class LLMOutputInvalid(BookingError):
    code = "LLM_OUTPUT_INVALID"


@runtime_checkable
class LLMClient(Protocol):
    def structured(self, request: LLMRequest, output_type: type[T]) -> LLMResult[T]: ...

    def text(self, request: LLMRequest) -> LLMResult[str]: ...
