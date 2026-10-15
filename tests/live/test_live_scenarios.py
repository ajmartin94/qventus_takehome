"""Demo scenarios with the real model reading and interpreting every turn. Spends API credit.

Skipped unless OR_BOOKING_LIVE=1 and an API key is available (environment or .env):

    OR_BOOKING_LIVE=1 .venv/Scripts/python -m pytest -m live
"""

from __future__ import annotations

import pytest

from or_booking.channels.scenario import load_scenario, run_scenario
from tests.conftest import PROJECT_ROOT

pytestmark = pytest.mark.live


def test_d1_runs_end_to_end_with_the_real_model() -> None:
    run = run_scenario(load_scenario(PROJECT_ROOT / "scenarios" / "demo" / "d1_faxed_request.yaml"), live=True)
    calls = [e.detail for e in run.audit if e.kind.value == "model_call"]
    assert all(c["outcome"] in ("ok", "fallback") for c in calls), calls
    assert run.passed, "\n".join(run.failures)
