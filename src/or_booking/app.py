"""Composition root: reads `config/app.yaml` and wires one adapter to each port.

This is the only module that imports adapters. Swapping the mock scheduling service
for a real integration is a new adapter, one entry in `ADAPTERS`, and one line of
configuration; the domain and orchestrator don't change.

`config/app.yaml` holds technical agent settings only (which adapter backs each port,
model and effort per prompt). Hospital rules are hospital data, read through ports.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict

from or_booking.interpretation import Interpreter, PromptRegistry, PromptSettings
from or_booking.observability import audited
from or_booking.orchestrator import Orchestrator, Ports
from or_booking.ports import (
    AuditLog,
    Clock,
    Directory,
    DocumentIngest,
    DurationHistory,
    EventSource,
    LLMClient,
    Outbox,
    PolicyStore,
    ReadinessHandoff,
    SchedulingService,
    Store,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class PortConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    adapter: str
    settings: dict[str, Any] = {}


class PromptModelSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    effort: Literal["low", "medium", "high", "max"]


class LLMSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default_model: str
    prompts: dict[str, PromptModelSettings] = {}


class ConversationSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_clarification_attempts: int = 3


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fixtures_dir: str
    prompts_dir: str = "prompts"
    ports: dict[str, PortConfig]
    llm: LLMSettings
    conversation: ConversationSettings = ConversationSettings()


def default_config_path() -> Path:
    """`$OR_BOOKING_CONFIG`, else the nearest `config/app.yaml` above the working directory, else the repo's."""
    if env := os.environ.get("OR_BOOKING_CONFIG"):
        return Path(env)
    for folder in (Path.cwd(), *Path.cwd().parents):
        candidate = folder / "config" / "app.yaml"
        if candidate.exists():
            return candidate
    return Path(__file__).resolve().parents[2] / "config" / "app.yaml"


def load_config(path: Path | None = None) -> tuple[AppConfig, Path]:
    """Returns the validated config and the project root that relative paths resolve against."""
    path = path or default_config_path()
    with path.open(encoding="utf-8") as f:
        config = AppConfig.model_validate(yaml.safe_load(f))
    return config, path.resolve().parent.parent


# ---------------------------------------------------------------------------
# Ports and the adapters that can back them
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PortSpec:
    name: str
    protocol: type
    audited: bool  # integration ports are wrapped so every call is recorded
    summary: str


PORTS: tuple[PortSpec, ...] = (
    PortSpec("clock", Clock, False, "Current time"),
    PortSpec("audit_log", AuditLog, False, "Every transition, model call and port call"),
    PortSpec("store", Store, False, "Requests and sessions across channels and hours"),
    PortSpec("scheduling", SchedulingService, True, "Availability, holds, bookings: the system of record"),
    PortSpec("directory", Directory, True, "Patients, orders, payers, surgeons, procedure master"),
    PortSpec("duration_history", DurationHistory, True, "Historical case durations"),
    PortSpec("policy_store", PolicyStore, True, "The hospital's structured policies"),
    PortSpec("document_ingest", DocumentIngest, True, "Fax, email and call intake as text"),
    PortSpec("event_source", EventSource, True, "Displaced-case, room-closure and time-opened events"),
    PortSpec("outbox", Outbox, True, "Notifications, drafted for approval"),
    PortSpec("readiness_handoff", ReadinessHandoff, True, "Readiness list to downstream follow-up"),
    # Model calls are recorded by the interpretation layer, with their prompt versions.
    PortSpec("llm", LLMClient, False, "Interpretation, extraction and phrasing"),
)


@dataclass(frozen=True)
class BuildContext:
    project_root: Path
    fixtures_dir: Path
    built: dict[str, Any]  # ports already wired, in PORTS order

    def path(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else self.project_root / p


Factory = Callable[[BuildContext, dict[str, Any]], Any]


def _frozen_clock(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.clock import FrozenClock

    return FrozenClock(datetime.fromisoformat(str(settings["at"])))


def _system_clock(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.clock import SystemClock

    return SystemClock()


def _jsonl_audit(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.audit_jsonl import JsonlAuditLog

    return JsonlAuditLog(ctx.path(settings.get("path", "var/audit.jsonl")))


def _memory_audit(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.audit_jsonl import MemoryAuditLog

    return MemoryAuditLog()


def _memory_store(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.store_memory import MemoryStore

    return MemoryStore()


def _sqlite_store(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.store_sqlite import SqliteStore

    return SqliteStore(ctx.path(settings.get("path", "var/requests.sqlite3")))


def _scripted_llm(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.llm_fake import ScriptedLLM

    return ScriptedLLM()


def _scheduling_mock(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.scheduling_mock import MockSchedulingService

    return MockSchedulingService.from_fixtures(ctx.fixtures_dir, clock=ctx.built["clock"])


def _directory_fixture(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.directory_fixture import FixtureDirectory

    return FixtureDirectory.from_fixtures(ctx.fixtures_dir)


def _history_csv(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.history_csv import CsvDurationHistory

    return CsvDurationHistory(ctx.fixtures_dir / "ehr" / "case_history.csv")


def _policy_store_fixture(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.policy_store_fixture import FixturePolicyStore

    return FixturePolicyStore(ctx.fixtures_dir / "policies")


def _ingest_fixture(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.ingest_fixture import FixtureDocumentIngest

    return FixtureDocumentIngest(ctx.fixtures_dir / "inbox", ctx.built["clock"])


def _events_simulated(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.events_simulated import SimulatedEventSource

    return SimulatedEventSource()


def _outbox_drafts(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.outbox_drafts import DraftOutbox

    return DraftOutbox(ctx.built["clock"])


def _readiness_recorded(ctx: BuildContext, settings: dict[str, Any]) -> Any:
    from or_booking.adapters.readiness_handoff import RecordedReadinessHandoff

    return RecordedReadinessHandoff(ctx.built["clock"])


# port name -> adapter name -> factory. Imports stay inside factories, so an adapter's
# vendor SDK is loaded only when configuration selects it.
ADAPTERS: dict[str, dict[str, Factory]] = {
    "clock": {"frozen": _frozen_clock, "system": _system_clock},
    "audit_log": {"jsonl": _jsonl_audit, "memory": _memory_audit},
    "store": {"memory": _memory_store, "sqlite": _sqlite_store},
    "scheduling": {"mock": _scheduling_mock},
    "directory": {"fixture": _directory_fixture},
    "duration_history": {"csv": _history_csv},
    "policy_store": {"fixture": _policy_store_fixture},
    "document_ingest": {"fixture": _ingest_fixture},
    "event_source": {"simulated": _events_simulated},
    "outbox": {"drafts": _outbox_drafts},
    "readiness_handoff": {"recorded": _readiness_recorded},
    "llm": {"scripted": _scripted_llm},
}


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------


class PortNotWired(RuntimeError):
    pass


class Unwired:
    """Placeholder for a port with no adapter configured. Fails loudly on first use."""

    def __init__(self, port: str) -> None:
        self._port = port

    def __getattr__(self, name: str) -> Any:
        raise PortNotWired(f"Port '{self._port}' has no adapter configured in config/app.yaml.")

    def __bool__(self) -> bool:
        return False


@dataclass
class Services:
    """Every port, wired. The orchestrator and channels receive this and nothing else."""

    config: AppConfig
    project_root: Path
    clock: Clock
    audit_log: AuditLog
    store: Store
    scheduling: SchedulingService
    directory: Directory
    duration_history: DurationHistory
    policy_store: PolicyStore
    document_ingest: DocumentIngest
    event_source: EventSource
    outbox: Outbox
    readiness_handoff: ReadinessHandoff
    llm: LLMClient
    wiring: dict[str, str] = field(default_factory=dict)  # port -> adapter name, or "-" if unwired


def build(
    config: AppConfig | None = None,
    *,
    project_root: Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> Services:
    """Wire every port. `overrides` replaces an adapter by port name (tests inject a clock this way)."""
    if config is None:
        config, root = load_config()
        project_root = project_root or root
    project_root = project_root or Path.cwd()
    overrides = overrides or {}
    ctx = BuildContext(project_root, project_root / config.fixtures_dir, built={})
    wiring: dict[str, str] = {}

    for spec in PORTS:
        if spec.name in overrides:
            adapter, wiring[spec.name] = overrides[spec.name], "override"
        elif spec.name in config.ports:
            port_config = config.ports[spec.name]
            factory = ADAPTERS.get(spec.name, {}).get(port_config.adapter)
            if factory is None:
                known = ", ".join(ADAPTERS.get(spec.name, {})) or "none yet"
                raise ValueError(f"Unknown adapter '{port_config.adapter}' for port '{spec.name}' (known: {known})")
            adapter, wiring[spec.name] = factory(ctx, port_config.settings), port_config.adapter
        else:
            ctx.built[spec.name], wiring[spec.name] = Unwired(spec.name), "-"
            continue
        if not isinstance(adapter, spec.protocol):
            raise TypeError(f"{type(adapter).__name__} does not implement port '{spec.name}'")
        if spec.audited:
            adapter = audited(spec.name, adapter, ctx.built["audit_log"], ctx.built["clock"])
        ctx.built[spec.name] = adapter

    for required in ("clock", "audit_log", "store"):
        if wiring[required] == "-":
            raise ValueError(f"Port '{required}' must be configured")
    return Services(config=config, project_root=project_root, wiring=wiring, **ctx.built)


def build_orchestrator(services: Services, coordinator_id: str = "C-0042") -> Orchestrator:
    """The agent: the orchestrator over the wired ports, with the interpreter and its prompts."""
    config = services.config
    interpreter = Interpreter(
        services.llm,
        PromptRegistry(services.project_root / config.prompts_dir),
        services.audit_log,
        services.clock,
        settings={name: PromptSettings(p.model, p.effort) for name, p in config.llm.prompts.items()},
        default_model=config.llm.default_model,
    )
    ports = Ports(
        clock=services.clock,
        audit_log=services.audit_log,
        store=services.store,
        scheduling=services.scheduling,
        directory=services.directory,
        duration_history=services.duration_history,
        policy_store=services.policy_store,
        document_ingest=services.document_ingest,
        event_source=services.event_source,
        outbox=services.outbox,
        readiness_handoff=services.readiness_handoff,
    )
    return Orchestrator(
        ports, interpreter, max_clarifications=config.conversation.max_clarification_attempts, coordinator_id=coordinator_id
    )
