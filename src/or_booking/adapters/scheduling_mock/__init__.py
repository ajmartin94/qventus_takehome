"""Mock OR scheduling system: holds with time limits, idempotent confirms, typed errors.

Reads fixtures/scheduling (the scheduling system's records) and fixtures/ehr (procedure
master, credentialing, patients), as a real scheduling system reads its own tables.
"""

from or_booking.adapters.scheduling_mock.service import MockSchedulingService

__all__ = ["MockSchedulingService"]
