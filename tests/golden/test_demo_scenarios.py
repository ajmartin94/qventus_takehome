"""Golden replays: every demo scenario runs end to end with the scripted model and meets its `expect` block.

If a change to code or fixture data breaks a demo story, this fails.
"""

from __future__ import annotations

import pytest

from or_booking.channels.scenario import load_scenario, run_scenario, scenario_paths
from tests.conftest import PROJECT_ROOT

DEMO = scenario_paths(PROJECT_ROOT / "scenarios" / "demo")


@pytest.mark.parametrize("path", DEMO, ids=[p.stem for p in DEMO])
def test_demo_scenario_replays(path) -> None:
    run = run_scenario(load_scenario(path))
    assert run.passed, "\n".join(run.failures)


def test_there_are_demo_scenarios() -> None:
    assert DEMO, "no scenarios in scenarios/demo"
