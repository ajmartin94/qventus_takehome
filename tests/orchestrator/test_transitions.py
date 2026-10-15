"""The documented state diagram is generated from the code's transition table, and can't drift from it."""

from __future__ import annotations

import re

from or_booking.orchestrator.states import TERMINAL, WAITING, State
from or_booking.orchestrator.transitions import TRANSITIONS, to_mermaid
from tests.conftest import PROJECT_ROOT


def _documented_diagram() -> str:
    doc = (PROJECT_ROOT / "docs" / "diagrams" / "booking_flow.md").read_text(encoding="utf-8")
    section = doc.split("## 3. Conversation state machine", 1)[1]
    match = re.search(r"```mermaid\n(.*?)```", section, re.S)
    assert match, "no mermaid block under '## 3. Conversation state machine'"
    return match.group(1).strip()


def test_state_diagram_in_the_docs_matches_the_transition_table() -> None:
    assert _documented_diagram() == to_mermaid().strip(), (
        "docs/diagrams/booking_flow.md section 3 has drifted from orchestrator/transitions.py; "
        "regenerate it with or_booking.orchestrator.transitions.to_mermaid()"
    )


def test_every_state_is_reachable_and_terminal_states_have_no_exits() -> None:
    targets = {t.target for t in TRANSITIONS}
    assert set(State) - {State.START} <= targets
    assert not [t for t in TRANSITIONS if t.source in TERMINAL]
    assert WAITING.isdisjoint(TERMINAL)
