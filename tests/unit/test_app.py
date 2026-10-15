"""Composition root, audit recording and the CLI entry point."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from or_booking.adapters.audit_jsonl import JsonlAuditLog, MemoryAuditLog
from or_booking.adapters.clock import FrozenClock
from or_booking.app import PORTS, PortConfig, PortNotWired, build, load_config
from or_booking.channels.cli import app as cli_app
from or_booking.domain.errors import NotFound
from or_booking.observability import audited, request_context
from or_booking.ports import AuditEntry, AuditKind
from tests.conftest import DEMO_NOW, PROJECT_ROOT


def test_config_wires_every_configured_port(services) -> None:
    assert services.clock.now() == DEMO_NOW
    assert set(services.wiring) == {spec.name for spec in PORTS}
    for name, adapter in services.wiring.items():
        if adapter == "-":
            with pytest.raises(PortNotWired):
                _ = getattr(services, name).anything


def test_unknown_adapter_is_rejected() -> None:
    config, root = load_config(PROJECT_ROOT / "config" / "app.yaml")
    config.ports["store"] = PortConfig(adapter="postgres")
    with pytest.raises(ValueError, match="Unknown adapter 'postgres' for port 'store'"):
        build(config, project_root=root)


def test_adapter_must_implement_its_port() -> None:
    config, root = load_config(PROJECT_ROOT / "config" / "app.yaml")
    with pytest.raises(TypeError, match="does not implement port 'clock'"):
        build(config, project_root=root, overrides={"clock": object()})


class _Directory:
    def get_patient(self, mrn: str) -> str:
        if mrn == "missing":
            raise NotFound("patient", mrn)
        return f"patient {mrn}"


def test_port_calls_are_recorded_with_request_and_outcome() -> None:
    log, clock = MemoryAuditLog(), FrozenClock(DEMO_NOW)
    directory = audited("directory", _Directory(), log, clock)

    with request_context("REQ-0001"):
        assert directory.get_patient("100231") == "patient 100231"
        with pytest.raises(NotFound):
            directory.get_patient("missing")

    ok, failed = log.entries("REQ-0001")
    assert (ok.kind, ok.name, ok.detail["args"], ok.detail["result"]) == (
        AuditKind.PORT_CALL,
        "directory.get_patient",
        ["100231"],
        "patient 100231",
    )
    assert failed.detail["error"]["code"] == "NOT_FOUND"


def test_jsonl_audit_log_round_trips(tmp_path) -> None:
    log = JsonlAuditLog(tmp_path / "audit.jsonl")
    log.record(AuditEntry(at=DEMO_NOW, request_id="REQ-1", kind=AuditKind.DECISION, name="x", detail={"a": 1}))
    log.record(AuditEntry(at=DEMO_NOW, request_id="REQ-2", kind=AuditKind.DECISION, name="y"))
    assert [e.name for e in log.entries("REQ-1")] == ["x"]
    assert len(log.entries()) == 2


def test_env_file_fills_gaps_but_never_overrides_the_environment(tmp_path, monkeypatch) -> None:
    from or_booking.app import load_env_file

    env = tmp_path / ".env"
    env.write_text("# comment\nOB_TEST_A=from-file\nexport OB_TEST_B='quoted'\nOB_TEST_C=\nOB_TEST_D=from-file\n", encoding="utf-8")
    for key in ("OB_TEST_A", "OB_TEST_B", "OB_TEST_C"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("OB_TEST_D", "from-environment")
    load_env_file(env)
    import os

    assert (os.environ["OB_TEST_A"], os.environ["OB_TEST_B"], os.environ["OB_TEST_D"]) == ("from-file", "quoted", "from-environment")
    assert "OB_TEST_C" not in os.environ  # an empty value would shadow other credential sources
    for key in ("OB_TEST_A", "OB_TEST_B"):
        monkeypatch.delenv(key)


def test_cli_starts() -> None:
    result = CliRunner().invoke(cli_app, ["ports"])
    assert result.exit_code == 0, result.output
    assert "scheduling" in result.output


def test_cli_shows_d1_availability_and_the_schedule() -> None:
    runner = CliRunner()
    availability = runner.invoke(cli_app, ["availability"], env={"COLUMNS": "200"})
    assert availability.exit_code == 0, availability.output
    assert "OPT-OR5-20261103-1300" in availability.output and "releases Oct 21 07:00" in availability.output
    refused = runner.invoke(cli_app, ["availability", "--surgeon", "S-CHEN"])
    assert refused.exit_code == 1 and "NOT_PRIVILEGED" in refused.output
    schedule = runner.invoke(cli_app, ["schedule"], env={"COLUMNS": "200"})
    assert schedule.exit_code == 0 and "TKA-ROBOTIC" in schedule.output


def test_cli_replays_d1_end_to_end_with_no_network() -> None:
    result = CliRunner().invoke(cli_app, ["replay", "d1"], env={"COLUMNS": "200"})
    assert result.exit_code == 0, result.output
    assert "Booked C-5001" in result.output and "PASS: demo-01-faxed-request" in result.output


def test_cli_chat_steps_through_a_scripted_conversation() -> None:
    result = CliRunner().invoke(cli_app, ["chat", "--scenario", "d1"], input="\n\n/sessions\n/drafts\n/quit\n", env={"COLUMNS": "200"})
    assert result.exit_code == 0, result.output
    assert "coordinator: DOB 3/12/1958, take Tuesday" in result.output and "Booked C-5001" in result.output
    assert "REQ-0001" in result.output and "D-0001" in result.output


def test_cli_free_chat_needs_a_live_model() -> None:
    result = CliRunner().invoke(cli_app, ["chat"])
    assert result.exit_code == 1 and "live model" in result.output
