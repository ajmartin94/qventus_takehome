"""Directory, duration history, policy store and the stub adapters over Northwind's data."""

from __future__ import annotations

import shutil
import statistics
from datetime import date, datetime

import pytest

from or_booking.adapters.clock import FrozenClock
from or_booking.adapters.directory_fixture import FixtureDirectory
from or_booking.adapters.events_simulated import SimulatedEventSource
from or_booking.adapters.fixture_data import FixtureError, load_ehr
from or_booking.adapters.history_csv import CsvDurationHistory
from or_booking.adapters.ingest_fixture import FixtureDocumentIngest
from or_booking.adapters.outbox_drafts import DraftOutbox
from or_booking.adapters.policy_store_fixture import FixturePolicyStore
from or_booking.domain.errors import NotFound, NotSupportedInPrototype
from or_booking.domain.models import Channel, Laterality
from or_booking.domain.policy import AutonomyMode, HospitalPolicies, Offset, Situation
from or_booking.ports.event_source import EventType, ScheduleEvent
from or_booking.ports.outbox import OutboundMessage
from tests.conftest import DEMO_NOW, FIXTURES

# --- Directory ---------------------------------------------------------------


@pytest.fixture(scope="module")
def directory() -> FixtureDirectory:
    return FixtureDirectory.from_fixtures(FIXTURES)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Robotic R TKA", ["TKA-ROBOTIC"]),  # the most specific alias wins
        ("R TKA", ["TKA"]),
        ("Total knee arthroplasty, robotic-assisted", ["TKA-ROBOTIC"]),
        ("27447", ["TKA-ROBOTIC", "TKA"]),  # one CPT code, two procedures: ambiguous
        ("TKA-ROBOTIC", ["TKA-ROBOTIC"]),
        ("lap chole", ["LAP-CHOLE"]),
        ("appendectomy", []),
    ],
)
def test_procedure_resolution(directory: FixtureDirectory, text: str, expected: list[str]) -> None:
    assert [p.id for p in directory.find_procedures(text)] == expected


def test_two_patients_named_maria_gomez(directory: FixtureDirectory) -> None:
    assert [p.mrn for p in directory.find_patients("Maria Gomez")] == ["100231", "100877"]
    assert [p.mrn for p in directory.find_patients("Maria Gomez", dob=date(1958, 3, 12))] == ["100231"]


@pytest.mark.parametrize(("name", "expected"), [("Dr. Patel", ["S-PATEL"]), ("P. Patel", ["S-PATEL"]), ("Dr. Smith", [])])
def test_surgeon_resolution(directory: FixtureDirectory, name: str, expected: list[str]) -> None:
    assert [s.id for s in directory.find_surgeons(name)] == expected


def test_orders_are_the_source_of_truth_for_side(directory: FixtureDirectory) -> None:
    (order,) = directory.orders_for_patient("100412")
    assert (order.procedure_id, order.laterality) == ("TKA", Laterality.RIGHT)
    with pytest.raises(NotFound):
        directory.get_patient("999999")


def test_inconsistent_ehr_fixtures_fail_at_startup(tmp_path) -> None:
    shutil.copytree(FIXTURES / "ehr", tmp_path / "ehr")
    orders = tmp_path / "ehr" / "orders.yaml"
    orders.write_text(orders.read_text(encoding="utf-8").replace("surgeon_id: S-LEE", "surgeon_id: S-NOBODY"), encoding="utf-8")
    with pytest.raises(FixtureError, match="unknown surgeon S-NOBODY"):
        load_ehr(tmp_path)


# --- Duration history --------------------------------------------------------


def test_history_sizes_the_demo_cases_exactly() -> None:
    history = CsvDurationHistory(FIXTURES / "ehr" / "case_history.csv")
    patel = history.surgeon_durations("S-PATEL", "TKA-ROBOTIC")
    assert len(patel) == 14 and statistics.median(patel) == 112
    assert statistics.quantiles(patel, n=10, method="inclusive")[7] == 135
    chen = history.surgeon_durations("S-CHEN", "TKA")
    assert len(chen) == 20 and statistics.median(chen) == 98
    # Thin history, so sizing's fallbacks get exercised
    assert len(history.surgeon_durations("S-PATEL", "UKA-ROBOTIC")) < 5
    assert len(history.procedure_durations("TIBIA-NAIL")) < 5


# --- Policy store ------------------------------------------------------------


def test_northwind_policies_load_as_the_four_rule_types() -> None:
    store = FixturePolicyStore(FIXTURES / "policies")
    policies = store.policies()

    urgent = policies.routing_for(Situation.URGENT_OR_EMERGENT)
    assert urgent and urgent.route_to == ["anesthesiologist_in_charge", "or_desk"] and not urgent.agent_continues
    assert policies.autonomy_for("book_case").tier == 2
    assert policies.autonomy_for("straight_through_booking").mode is AutonomyMode.SHADOW
    loaner = next(r for r in policies.readiness if r.id == "loaner_set_in_spd")
    assert loaner.due.before_surgery == Offset(hours=48)
    assert loaner.variants[0].due.before_surgery == Offset(business_days=3)
    assert {s for s in Situation} == {r.situation for r in policies.routing}, "every situation has a route"

    with pytest.raises(NotSupportedInPrototype) as stub:
        store.search("when does a robotic block release?")
    assert stub.value.routes_to == "coordinator"


def test_policies_with_dangling_references_are_rejected() -> None:
    rule = {"id": "financial_clearance", "item": "x", "owner": "y", "depends_on": ["no_such_item"], "source": "z"}
    with pytest.raises(ValueError, match="unknown items"):
        HospitalPolicies.model_validate({"booking": [], "readiness": [rule], "routing": [], "autonomy": []})
    with pytest.raises(ValueError, match="exactly one"):
        Offset(hours=48, days=2)


# --- Stubs -------------------------------------------------------------------


def test_inbox_shows_documents_once_received() -> None:
    clock = FrozenClock(DEMO_NOW)
    inbox = FixtureDocumentIngest(FIXTURES / "inbox", clock)
    assert [d.document_id for d in inbox.list_documents()] == ["fax_001", "email_002", "email_003"]
    assert "Robotic R TKA" in inbox.get_document("fax_001").text
    with pytest.raises(NotFound):
        inbox.get_document("fax_004")  # the late reply hasn't arrived at 09:00
    clock.set(datetime(2026, 10, 14, 13, 30))
    assert inbox.get_document("fax_004").channel is Channel.FAX


def test_outbox_only_drafts_and_events_deliver_once() -> None:
    outbox = DraftOutbox(FrozenClock(DEMO_NOW))
    draft = outbox.draft(OutboundMessage(request_id="REQ-1", recipient_role="surgeons_office", channel=Channel.FAX, subject="s", body="b"))
    assert draft.status == "draft" and outbox.drafts("REQ-1") == [draft] and outbox.drafts("REQ-2") == []

    events = SimulatedEventSource()
    events.inject(ScheduleEvent(event_id="E-1", type=EventType.CASE_DISPLACED, occurred_at=DEMO_NOW, case_ids=["C-4417"]))
    assert [e.event_id for e in events.poll()] == ["E-1"]
    assert events.poll() == []
