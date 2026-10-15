"""The Anthropic adapter against a stubbed SDK client: request shape, stop reasons, errors. No network."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import anthropic
import httpx2
import pytest

from or_booking.adapters.audit_jsonl import MemoryAuditLog
from or_booking.adapters.clock import FrozenClock
from or_booking.adapters.llm_anthropic import FALLBACK_BETA, AnthropicLLM
from or_booking.interpretation import Intent, Interpreter, PromptRegistry, PromptSettings, TurnContext, TurnInterpretation
from or_booking.ports.llm import LLMOutputInvalid, LLMRequest, LLMUnavailable
from tests.conftest import DEMO_NOW, PROJECT_ROOT

REQUEST = LLMRequest(prompt_id="interpret_turn", prompt_version="v1", system="stable rules", user="<message>take Tuesday</message>",
                     model="claude-opus-5-5", effort="medium")  # fmt: skip


def response(stop_reason: str = "end_turn", parsed: Any = None, text: str = "", model: str = "claude-opus-5-5") -> SimpleNamespace:
    return SimpleNamespace(
        stop_reason=stop_reason,
        model=model,
        parsed_output=parsed,
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
        usage=SimpleNamespace(input_tokens=1200, output_tokens=80, cache_read_input_tokens=900, cache_creation_input_tokens=None),
    )


class StubMessages:
    def __init__(self, result: Any = None, error: Exception | None = None) -> None:
        self.result, self.error, self.calls = result, error, []

    def _respond(self, kind: str, kwargs: dict[str, Any]) -> Any:
        self.calls.append((kind, kwargs))
        if self.error:
            raise self.error
        return self.result

    def parse(self, **kwargs: Any) -> Any:
        return self._respond("parse", kwargs)

    def create(self, **kwargs: Any) -> Any:
        return self._respond("create", kwargs)


def adapter(messages: StubMessages, **options: Any) -> AnthropicLLM:
    return AnthropicLLM(client=SimpleNamespace(beta=SimpleNamespace(messages=messages)), **options)


def test_structured_request_is_schema_constrained_cached_and_has_fallbacks() -> None:
    messages = StubMessages(response(parsed=TurnInterpretation(intent=Intent.SELECT_OPTION, selected_option=1)))
    result = adapter(messages).structured(REQUEST, TurnInterpretation)

    ((kind, sent),) = messages.calls
    assert kind == "parse" and sent["output_format"] is TurnInterpretation
    assert sent["model"] == "claude-opus-5-5" and sent["max_tokens"] == 16000
    assert sent["output_config"] == {"effort": "medium"} and "thinking" not in sent  # Opus 5.5 always thinks; effort is the control
    assert sent["system"] == [{"type": "text", "text": "stable rules", "cache_control": {"type": "ephemeral"}}]
    assert sent["messages"] == [{"role": "user", "content": "<message>take Tuesday</message>"}]
    assert (sent["betas"], sent["fallbacks"]) == ([FALLBACK_BETA], "default")

    assert result.value.selected_option == 1 and not result.refused
    assert (result.usage.input_tokens, result.usage.cache_read_tokens, result.usage.cache_write_tokens) == (1200, 900, 0)


@pytest.mark.parametrize("stop_reason", ["refusal", "max_tokens"])
def test_refused_or_truncated_output_is_never_used(stop_reason: str) -> None:
    parsed = TurnInterpretation(intent=Intent.CONFIRM)
    result = adapter(StubMessages(response(stop_reason=stop_reason, parsed=parsed))).structured(REQUEST, TurnInterpretation)
    assert result.value is None and result.stop_reason == stop_reason and result.refused is (stop_reason == "refusal")


def test_text_calls_return_the_text_blocks_and_report_who_served_them() -> None:
    messages = StubMessages(response(text=" Two options. ", model="claude-opus-4-8"))
    result = adapter(messages).text(REQUEST)
    assert messages.calls[0][0] == "create" and result.value == "Two options." and result.model == "claude-opus-4-8"


def test_fallbacks_can_be_turned_off() -> None:
    messages = StubMessages(response(text="ok"))
    adapter(messages, fallbacks=None).text(REQUEST)
    assert "betas" not in messages.calls[0][1] and "fallbacks" not in messages.calls[0][1]


_REQ = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (anthropic.APIConnectionError(request=_REQ), LLMUnavailable),
        (anthropic.BadRequestError("bad schema", response=httpx2.Response(400, request=_REQ), body=None), LLMUnavailable),
        (anthropic.AuthenticationError("bad key", response=httpx2.Response(401, request=_REQ), body=None), LLMUnavailable),
        (anthropic.InternalServerError("boom", response=httpx2.Response(500, request=_REQ), body=None), LLMUnavailable),
        (ValueError("not valid JSON for the schema"), LLMOutputInvalid),
    ],
    ids=["connection", "bad_request", "auth", "server", "invalid_output"],
)
def test_api_failures_become_the_ports_typed_errors(error: Exception, expected: type) -> None:
    with pytest.raises(expected):
        adapter(StubMessages(error=error)).structured(REQUEST, TurnInterpretation)


def test_the_interpreter_asks_a_person_when_the_model_refuses() -> None:
    audit = MemoryAuditLog()
    llm = adapter(StubMessages(response(stop_reason="refusal")))
    interpreter = Interpreter(
        llm, PromptRegistry(PROJECT_ROOT / "prompts"), audit, FrozenClock(DEMO_NOW),
        {"interpret_turn": PromptSettings("claude-opus-5-5", "medium")}, default_model="claude-opus-5-5",
    )  # fmt: skip
    assert interpreter.interpret_turn(TurnContext(state="Presenting"), "take Tuesday") is None
    (entry,) = audit.entries()
    assert entry.detail["outcome"] == "unusable" and entry.detail["refused"] is True
