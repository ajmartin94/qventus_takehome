"""LLMClient over the Anthropic API. The only module that imports the Anthropic SDK.

- Structured calls use `beta.messages.parse` with the Pydantic schema as `output_format`,
  so the response is constrained to the schema and validated into the model.
- Effort is set per call (`output_config.effort`); Claude Opus 5.5 always thinks
  adaptively, so there is no thinking parameter to send.
- The system prompt is stable and goes first, marked for caching; per-request state goes
  last, in the user message.
- `stop_reason` is checked before content: a refusal or a truncated response comes back
  as `refused` / `value=None`, never as a guess.
- Server-side fallbacks are on by default: if a safety classifier declines a request,
  the API re-runs it on Anthropic's recommended fallback model within the same call.
- API failures become the port's typed errors (`LLMUnavailable`, `LLMOutputInvalid`); the
  SDK already retries connection errors, 429s and 5xx responses.
"""

from __future__ import annotations

from typing import Any, TypeVar

import anthropic
from pydantic import BaseModel, ValidationError

from or_booking.ports.llm import LLMOutputInvalid, LLMRequest, LLMResult, LLMUnavailable, TokenUsage

T = TypeVar("T")

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class AnthropicLLM:
    def __init__(
        self,
        client: Any | None = None,
        *,
        default_model: str = "claude-opus-5-5",
        max_tokens: int = 16000,
        fallbacks: str | None = "default",
        timeout: float = 120.0,
        max_retries: int = 2,
    ) -> None:
        # Credentials resolve from the environment (ANTHROPIC_API_KEY or an `ant auth login` profile).
        self._client = client or anthropic.Anthropic(timeout=timeout, max_retries=max_retries)
        self._default_model = default_model
        self._max_tokens = max_tokens
        self._fallbacks = fallbacks

    def structured(self, request: LLMRequest, output_type: type[T]) -> LLMResult[T]:
        if not (isinstance(output_type, type) and issubclass(output_type, BaseModel)):
            raise TypeError("structured output needs a Pydantic model type")
        response = self._call(lambda: self._client.beta.messages.parse(output_format=output_type, **self._params(request)))
        result = self._result(response, value=None)
        if result.refused or response.stop_reason != "end_turn":
            return result
        return result.model_copy(update={"value": response.parsed_output})

    def text(self, request: LLMRequest) -> LLMResult[str]:
        response = self._call(lambda: self._client.beta.messages.create(**self._params(request)))
        result = self._result(response, value=None)
        if result.refused or response.stop_reason != "end_turn":
            return result
        text = "".join(block.text for block in response.content if block.type == "text").strip()
        return result.model_copy(update={"value": text, "text": text})

    # ------------------------------------------------------------------

    def _params(self, request: LLMRequest) -> dict[str, Any]:
        params: dict[str, Any] = {
            "model": request.model or self._default_model,
            "max_tokens": request.max_tokens or self._max_tokens,
            # Stable instructions first, cached; the per-request state and message last.
            "system": [{"type": "text", "text": request.system, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": request.user}],
        }
        if request.effort:
            params["output_config"] = {"effort": request.effort}
        if self._fallbacks:
            params["betas"] = [FALLBACK_BETA]
            params["fallbacks"] = self._fallbacks
        return params

    @staticmethod
    def _result(response: Any, value: Any) -> LLMResult[Any]:
        usage = response.usage
        return LLMResult(
            value=value,
            stop_reason=response.stop_reason,
            refused=response.stop_reason == "refusal",
            model=response.model,  # the model that served it: a fallback model if one ran
            usage=TokenUsage(
                input_tokens=usage.input_tokens or 0,
                output_tokens=usage.output_tokens or 0,
                cache_read_tokens=getattr(usage, "cache_read_input_tokens", None) or 0,
                cache_write_tokens=getattr(usage, "cache_creation_input_tokens", None) or 0,
            ),
        )

    @staticmethod
    def _call(make_request: Any) -> Any:
        try:
            return make_request()
        except anthropic.APIConnectionError as err:  # includes timeouts, after the SDK's retries
            raise LLMUnavailable(f"Couldn't reach the model: {err}") from err
        except anthropic.RateLimitError as err:
            raise LLMUnavailable("Rate limited by the API after retries", status=429) from err
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError) as err:
            raise LLMUnavailable(f"API credentials rejected: {err.message}", status=err.status_code) from err
        except anthropic.BadRequestError as err:
            raise LLMUnavailable(f"API rejected the request: {err.message}", status=400) from err
        except anthropic.APIStatusError as err:
            raise LLMUnavailable(f"API error {err.status_code}: {err.message}", status=err.status_code) from err
        except (ValidationError, ValueError) as err:  # output that doesn't validate against the schema
            raise LLMOutputInvalid(f"Model output didn't match the schema: {err}") from err
