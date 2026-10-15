from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pytest

from or_booking.adapters.audit_jsonl import MemoryAuditLog
from or_booking.adapters.clock import FrozenClock
from or_booking.app import Services, build, load_config

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PROJECT_ROOT / "fixtures"
DEMO_NOW = datetime(2026, 10, 14, 9, 0)


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Live tests spend API credit: they run only when asked for, with a key available."""
    load_config(PROJECT_ROOT / "config" / "app.yaml")  # loads .env
    if os.environ.get("OR_BOOKING_LIVE") == "1" and os.environ.get("ANTHROPIC_API_KEY"):
        return
    skip = pytest.mark.skip(reason="live model test: set OR_BOOKING_LIVE=1 and ANTHROPIC_API_KEY (environment or .env)")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip)


@pytest.fixture
def clock() -> FrozenClock:
    return FrozenClock(DEMO_NOW)


@pytest.fixture
def services(clock: FrozenClock) -> Services:
    """Everything wired from config/app.yaml, with a frozen clock and an in-memory audit log."""
    config, root = load_config(PROJECT_ROOT / "config" / "app.yaml")
    return build(config, project_root=root, overrides={"clock": clock, "audit_log": MemoryAuditLog()})
