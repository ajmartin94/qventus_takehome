"""PolicyStore adapter over the simulated hospital's policy files (fixtures/policies).

Structured rules come from the four YAML files and are what the agent enforces. Passage
search over the prose versions (*.md), for citations, is a stretch goal; until then
`search` says so rather than returning nothing.
"""

from __future__ import annotations

from pathlib import Path

from or_booking.adapters.fixture_data import parse, read_yaml
from or_booking.domain.errors import NotSupportedInPrototype
from or_booking.domain.policy import HospitalPolicies
from or_booking.ports.policy_store import PolicyPassage


class FixturePolicyStore:
    def __init__(self, policies_dir: Path) -> None:
        self._dir = policies_dir
        data = {kind: read_yaml(policies_dir / f"{kind}.yaml") for kind in ("booking", "readiness", "routing", "autonomy")}
        self._policies = parse(policies_dir, data, HospitalPolicies)

    def policies(self) -> HospitalPolicies:
        return self._policies

    def search(self, query: str, limit: int = 3) -> list[PolicyPassage]:
        raise NotSupportedInPrototype(
            "policy passage search",
            routes_to="coordinator",
            detail=f"BM25 over {self._dir.name}/*.md is a stretch goal; structured rules are unaffected.",
        )
