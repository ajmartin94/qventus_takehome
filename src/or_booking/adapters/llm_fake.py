"""Scripted LLM for replay mode and tests: returns queued outputs, never calls a network.

Structured calls return the next output queued for that prompt id; running out is a
test bug and fails loudly. Text calls return queued text if any, else nothing, so the
interpreter falls back to the code's own wording and replay transcripts stay
deterministic.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, TypeVar

from pydantic import BaseModel

from or_booking.ports.llm import LLMRequest, LLMResult

T = TypeVar("T")


class ScriptExhausted(AssertionError):
    """A structured call arrived with nothing scripted for it."""


class ScriptedLLM:
    def __init__(self) -> None:
        self._structured: dict[str, deque[Any]] = defaultdict(deque)
        self._texts: dict[str, deque[str]] = defaultdict(deque)
        self.calls: list[LLMRequest] = []

    def queue(self, prompt_id: str, *outputs: Any) -> None:
        """Queue structured outputs (models or plain dicts) for a prompt id, in order."""
        self._structured[prompt_id].extend(outputs)

    def queue_text(self, prompt_id: str, *texts: str) -> None:
        self._texts[prompt_id].extend(texts)

    def remaining(self) -> dict[str, int]:
        return {k: len(v) for k, v in self._structured.items() if v}

    def structured(self, request: LLMRequest, output_type: type[T]) -> LLMResult[T]:
        self.calls.append(request)
        pending = self._structured[request.prompt_id]
        if not pending:
            raise ScriptExhausted(f"Nothing scripted for {request.prompt_id}; the scenario needs another scripted output")
        output = pending.popleft()
        if not isinstance(output, output_type) and issubclass(output_type, BaseModel):  # type: ignore[arg-type]
            output = output_type.model_validate(output)  # type: ignore[attr-defined]
        return LLMResult(value=output, stop_reason="end_turn", model="scripted")

    def text(self, request: LLMRequest) -> LLMResult[str]:
        self.calls.append(request)
        pending = self._texts[request.prompt_id]
        if pending:
            return LLMResult(value=pending.popleft(), stop_reason="end_turn", model="scripted")
        return LLMResult(value=None, stop_reason="not_scripted", model="scripted")
