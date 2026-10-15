"""Ports: the typed contracts between the core and the outside world.

Each port is a `Protocol` with Pydantic request/response models and a defined set of
typed errors (`or_booking.domain.errors`). The orchestrator depends on these; adapters
implement them; only the composition root connects the two.
"""

from or_booking.ports.audit_log import AuditEntry, AuditKind, AuditLog
from or_booking.ports.clock import Clock
from or_booking.ports.directory import Directory
from or_booking.ports.document_ingest import DocumentIngest, InboundDocument
from or_booking.ports.duration_history import DurationHistory
from or_booking.ports.event_source import EventSource, EventType, ScheduleEvent
from or_booking.ports.llm import LLMClient, LLMRequest, LLMResult
from or_booking.ports.outbox import DraftRecord, OutboundMessage, Outbox
from or_booking.ports.policy_store import PolicyPassage, PolicyStore
from or_booking.ports.readiness_handoff import HandoffReceipt, ReadinessHandoff
from or_booking.ports.scheduling import ScheduleView, SchedulingService
from or_booking.ports.store import Store

__all__ = [
    "AuditEntry",
    "AuditKind",
    "AuditLog",
    "Clock",
    "Directory",
    "DocumentIngest",
    "DraftRecord",
    "DurationHistory",
    "EventSource",
    "EventType",
    "HandoffReceipt",
    "InboundDocument",
    "LLMClient",
    "LLMRequest",
    "LLMResult",
    "OutboundMessage",
    "Outbox",
    "PolicyPassage",
    "PolicyStore",
    "ReadinessHandoff",
    "ScheduleEvent",
    "ScheduleView",
    "SchedulingService",
    "Store",
]
