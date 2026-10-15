"""Prompt registry: versioned templates loaded by id, assembled from shared fragments.

A prompt lives in `prompts/<id>.<version>.md` with a `## System` part and a `## User`
part. The system part is stable (role, definitions, rules) so it caches; per-request
state goes in the user part. Template syntax, kept deliberately small:

- `{{> role}}` includes the fragment `prompts/_role.md`
- `{{fields}}` and `{{intents}}` are generated from the code's own definitions, so the
  prompt's vocabulary can't drift from the schema the validators use
- `{{name}}` is a variable; a missing one is an error, never an empty string
"""

from __future__ import annotations

import re
from pathlib import Path

from or_booking.domain.models import FIELD_DEFINITIONS
from or_booking.interpretation.schemas import INTENT_DEFINITIONS

_INCLUDE = re.compile(r"\{\{>\s*([a-z_]+)\s*\}\}")
_VARIABLE = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")


def field_definitions() -> str:
    return "\n".join(f"- `{field.value}`: {text}" for field, text in FIELD_DEFINITIONS.items())


def intent_definitions() -> str:
    return "\n".join(f"- `{intent.value}`: {text}" for intent, text in INTENT_DEFINITIONS.items())


class PromptRegistry:
    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def render(self, prompt_id: str, version: str = "v1", **variables: str) -> tuple[str, str]:
        """Returns (system, user) for the prompt, with fragments and variables filled in."""
        path = self._dir / f"{prompt_id}.{version}.md"
        if not path.exists():
            raise FileNotFoundError(f"No prompt {prompt_id} {version} at {path}")
        text = _INCLUDE.sub(lambda m: self._fragment(m.group(1)), path.read_text(encoding="utf-8"))
        builtins = {"fields": field_definitions(), "intents": intent_definitions()}

        def fill(m: re.Match[str]) -> str:
            name = m.group(1)
            if name in builtins:
                return builtins[name]
            if name not in variables:
                raise KeyError(f"prompt {prompt_id} {version} needs variable '{name}'")
            return variables[name]

        system, _, user = text.partition("\n## User\n")
        if not user:
            raise ValueError(f"prompt {prompt_id} {version} has no '## User' part")
        system = system.removeprefix("## System\n").strip()
        return _VARIABLE.sub(fill, system), _VARIABLE.sub(fill, user).strip()

    def _fragment(self, name: str) -> str:
        path = self._dir / f"_{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"No prompt fragment _{name}.md in {self._dir}")
        return path.read_text(encoding="utf-8").strip()
