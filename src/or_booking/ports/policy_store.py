"""PolicyStore port: the hospital's perioperative policies.

`policies()` serves the structured rules the agent enforces (the four rule types).
`search()` finds passages in the prose versions, for citations and explanations only;
prose is never used for enforcement.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from or_booking.domain.models import Model
from or_booking.domain.policy import HospitalPolicies


class PolicyPassage(Model):
    document: str
    section: str
    text: str
    score: float


@runtime_checkable
class PolicyStore(Protocol):
    def policies(self) -> HospitalPolicies: ...

    def search(self, query: str, limit: int = 3) -> list[PolicyPassage]: ...
