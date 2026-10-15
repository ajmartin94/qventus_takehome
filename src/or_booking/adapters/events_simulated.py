"""EventSource stub: events are injected (from the CLI or a scenario) and polled once.

Stands in for an HL7 SIU scheduling feed or EHR webhooks. A real adapter would map
SIU^S12/S13/S14/S15 messages (new, reschedule, modify, cancel) and room or equipment
status changes onto `ScheduleEvent`, de-duplicate them, and acknowledge each one.
"""

from __future__ import annotations

from or_booking.ports.event_source import ScheduleEvent


class SimulatedEventSource:
    def __init__(self) -> None:
        self._pending: list[ScheduleEvent] = []

    def inject(self, event: ScheduleEvent) -> None:
        """Simulation hook, not part of the port: queue an event as if the feed delivered it."""
        self._pending.append(event)

    def poll(self) -> list[ScheduleEvent]:
        delivered, self._pending = sorted(self._pending, key=lambda e: e.occurred_at), []
        return delivered
