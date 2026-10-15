"""The model's three jobs, behind one class: interpret a turn, extract a document, phrase a reply.

The interpreter never decides anything. It returns proposed values for the state machine
to check, or a line of text built only from facts the code produced. Every call is
recorded with its prompt version. A refusal, an error or an unusable response becomes
`None` (interpretation) or the code's own fallback text (phrasing), so the flow asks the
coordinator instead of guessing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, TypeVar

from pydantic import BaseModel

from or_booking.domain.errors import BookingError
from or_booking.interpretation.prompts import PromptRegistry
from or_booking.interpretation.schemas import ExtractedRequest, TurnContext, TurnInterpretation
from or_booking.ports.audit_log import AuditEntry, AuditKind, AuditLog
from or_booking.ports.clock import Clock
from or_booking.ports.document_ingest import InboundDocument
from or_booking.ports.llm import LLMClient, LLMRequest, LLMResult
from or_booking.observability import current_request_id

T = TypeVar("T", bound=BaseModel)

# Prompt versions in use. An eval run pins these; every call logs the one it used.
PROMPT_VERSIONS = {
    "interpret_turn": "v1",
    "extract_document": "v1",
    "ask_clarification": "v1",
    "explain_options": "v1",
    "summarize_outcome": "v1",
}


@dataclass(frozen=True)
class PromptSettings:
    model: str
    effort: str


def _as_data(text: str) -> str:
    """Neutralize closing tags so text inside a data block can't end the block early."""
    return text.replace("</", "<\\/")


class Interpreter:
    def __init__(
        self,
        llm: LLMClient,
        prompts: PromptRegistry,
        audit_log: AuditLog,
        clock: Clock,
        settings: dict[str, PromptSettings],
        default_model: str,
    ) -> None:
        self._llm = llm
        self._prompts = prompts
        self._audit = audit_log
        self._clock = clock
        self._settings = settings
        self._default_model = default_model

    def interpret_turn(self, context: TurnContext, message: str) -> TurnInterpretation | None:
        request = self._request(
            "interpret_turn", state=context.model_dump_json(indent=2), message=_as_data(message)
        )
        return self._structured(request, TurnInterpretation)

    def extract_document(self, document: InboundDocument) -> ExtractedRequest | None:
        request = self._request(
            "extract_document",
            channel=document.channel.value,
            received_at=document.received_at.isoformat(timespec="minutes"),
            sender=document.sender or "unknown",
            document=_as_data(document.text),
        )
        return self._structured(request, ExtractedRequest)

    def phrase(self, prompt_id: str, facts: dict[str, Any], fallback: str) -> str:
        request = self._request(prompt_id, facts=json.dumps(facts, indent=2, default=str))
        try:
            result = self._llm.text(request)
        except BookingError as err:
            self._record(request, None, outcome=f"fallback ({err.code})")
            return fallback
        text = (result.value or "").strip()
        usable = bool(text) and not result.refused and result.stop_reason in (None, "end_turn")
        self._record(request, result, outcome="ok" if usable else "fallback")
        return text if usable else fallback

    # ------------------------------------------------------------------

    def _request(self, prompt_id: str, **variables: str) -> LLMRequest:
        version = PROMPT_VERSIONS[prompt_id]
        system, user = self._prompts.render(prompt_id, version, **variables)
        settings = self._settings.get(prompt_id)
        return LLMRequest(
            prompt_id=prompt_id,
            prompt_version=version,
            system=system,
            user=user,
            model=settings.model if settings else self._default_model,
            effort=settings.effort if settings else None,  # type: ignore[arg-type]
        )

    def _structured(self, request: LLMRequest, output_type: type[T]) -> T | None:
        try:
            result = self._llm.structured(request, output_type)
        except BookingError as err:
            self._record(request, None, outcome=f"failed ({err.code})")
            return None
        if result.refused or result.value is None or result.stop_reason not in (None, "end_turn"):
            self._record(request, result, outcome="unusable")
            return None
        self._record(request, result, outcome="ok")
        return result.value

    def _record(self, request: LLMRequest, result: LLMResult[Any] | None, outcome: str) -> None:
        detail: dict[str, Any] = {
            "prompt": request.prompt_id,
            "version": request.prompt_version,
            "model": request.model,
            "effort": request.effort,
            "outcome": outcome,
        }
        if result is not None:
            detail |= {
                "served_by": result.model,
                "stop_reason": result.stop_reason,
                "refused": result.refused,
                "usage": result.usage.model_dump(),
            }
            if isinstance(result.value, BaseModel):
                detail["output"] = result.value.model_dump(mode="json")
        self._audit.record(
            AuditEntry(
                at=self._clock.now(),
                request_id=current_request_id.get(),
                kind=AuditKind.MODEL_CALL,
                name=f"llm.{request.prompt_id}",
                detail=detail,
            )
        )
