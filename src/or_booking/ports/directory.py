"""Directory port: EHR patient search and orders, payer records, credentialing, procedure master.

`find_*` methods take words as a person wrote them and return every match; the caller
decides what an ambiguous result means. `get_*` methods take an identifier and raise
`NotFound` if it doesn't exist. Identifiers only ever come from here, never from the model.
"""

from __future__ import annotations

from datetime import date
from typing import Protocol, runtime_checkable

from or_booking.domain.models import Patient, Payer, Procedure, Surgeon, SurgicalOrder


@runtime_checkable
class Directory(Protocol):
    def find_surgeons(self, name: str) -> list[Surgeon]: ...

    def get_surgeon(self, surgeon_id: str) -> Surgeon: ...

    def find_procedures(self, text: str) -> list[Procedure]: ...

    def get_procedure(self, procedure_id: str) -> Procedure: ...

    def find_patients(self, name: str, dob: date | None = None) -> list[Patient]: ...

    def get_patient(self, mrn: str) -> Patient: ...

    def orders_for_patient(self, mrn: str) -> list[SurgicalOrder]: ...

    def get_payer(self, payer_id: str) -> Payer: ...
