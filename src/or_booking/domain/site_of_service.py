"""Site of service: which setting may perform a case (surgery center, hospital outpatient, main OR). Stub.

Designed, not built. Eligibility depends on payer rules (for example Medicare's
ambulatory surgery center covered procedures list), the hospital's own lists and the
patient's risk class. Those are hospital and payer data, so a real gate would read them
through a port and evaluate them like any other policy. The prototype has one setting,
Northwind's main OR.
"""

from __future__ import annotations

from or_booking.domain.models import Patient, Payer, Procedure, Unsupported


def eligible_settings(procedure: Procedure, payer: Payer | None, patient: Patient | None) -> Unsupported:
    return Unsupported(
        capability="Site-of-service eligibility",
        reason=f"Choosing between settings for {procedure.id} isn't supported; the prototype books Northwind's main OR",
        would_need=["payer eligibility lists", "hospital setting lists", "patient risk class"],
    )
