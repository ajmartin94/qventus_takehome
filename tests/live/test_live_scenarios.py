"""Demo scenarios with the real model reading and interpreting every turn. Spends API credit (about $0.50 for all seven).

Skipped unless OR_BOOKING_LIVE=1 and an API key is available (environment or .env):

    OR_BOOKING_LIVE=1 .venv/Scripts/python -m pytest -m live
"""

from __future__ import annotations

import pytest

from or_booking.channels.scenario import load_scenario, run_scenario, scenario_paths
from tests.conftest import PROJECT_ROOT

pytestmark = pytest.mark.live

DEMO = scenario_paths(PROJECT_ROOT / "scenarios" / "demo")


@pytest.mark.parametrize("path", DEMO, ids=[p.stem for p in DEMO])
def test_demo_scenario_runs_with_the_real_model(path) -> None:
    run = run_scenario(load_scenario(path), live=True)
    calls = [e.detail for e in run.audit if e.kind.value == "model_call"]
    assert all(c["outcome"] in ("ok", "fallback") for c in calls), calls
    assert run.passed, "\n".join(run.failures)
