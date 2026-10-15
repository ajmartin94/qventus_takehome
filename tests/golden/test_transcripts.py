"""The committed transcripts in docs/demo/ are exactly what the code produces now."""

from __future__ import annotations

import pytest

from or_booking.channels.transcript import demo_transcripts
from tests.conftest import PROJECT_ROOT

PAGES = demo_transcripts(PROJECT_ROOT / "scenarios" / "demo", PROJECT_ROOT / "docs" / "demo")


@pytest.mark.parametrize("path", sorted(PAGES), ids=[p.name for p in sorted(PAGES)])
def test_committed_transcript_is_current(path) -> None:
    assert path.exists(), f"{path.name} is missing; run `or-booking transcripts`"
    assert path.read_text(encoding="utf-8") == PAGES[path], f"{path.name} has drifted from the code; run `or-booking transcripts`"
