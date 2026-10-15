"""Directory adapter over the simulated EHR (fixtures/ehr).

Stands in for EHR patient search and orders, payer records, credentialing and the
procedure master. Matching is deliberately literal, like a real search box: it returns
every candidate and leaves ambiguity to the caller.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from or_booking.adapters.fixture_data import EhrRecords, load_ehr
from or_booking.domain.errors import NotFound
from or_booking.domain.models import Patient, Payer, Procedure, Surgeon, SurgicalOrder

# Words that say which side, not which operation. Laterality is resolved separately.
_SIDE_WORDS = {"r", "l", "rt", "lt", "right", "left", "bilateral", "bilat", "b"}
_TITLE_WORDS = {"dr", "doctor", "md"}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class FixtureDirectory:
    def __init__(self, records: EhrRecords) -> None:
        self._r = records

    @classmethod
    def from_fixtures(cls, fixtures_dir: Path) -> FixtureDirectory:
        return cls(load_ehr(fixtures_dir))

    # Surgeons ---------------------------------------------------------------

    def find_surgeons(self, name: str) -> list[Surgeon]:
        """'Dr. Priya Patel', 'Patel', 'P. Patel' all match; every query word must match a name word or initial."""
        words = [w for w in _tokens(name) if w not in _TITLE_WORDS]
        if not words:
            return []

        def matches(s: Surgeon) -> bool:
            names = [s.first_name.lower(), s.last_name.lower()]
            return all(any(w == n or (len(w) == 1 and n.startswith(w)) for n in names) for w in words)

        return [s for s in self._r.surgeons.values() if matches(s)]

    def get_surgeon(self, surgeon_id: str) -> Surgeon:
        if surgeon_id not in self._r.surgeons:
            raise NotFound("surgeon", surgeon_id)
        return self._r.surgeons[surgeon_id]

    # Procedures -------------------------------------------------------------

    def find_procedures(self, text: str) -> list[Procedure]:
        """Match a CPT code, a procedure id, or the most specific alias contained in the text.

        'Robotic R TKA' matches TKA-ROBOTIC (alias 'robotic tka') rather than TKA (alias
        'tka'), because the longer alias is fully present. Ties return every candidate.
        """
        stripped = text.strip()
        if re.fullmatch(r"\d{5}", stripped):
            return [p for p in self._r.procedures.values() if p.cpt == stripped]
        if stripped.upper() in self._r.procedures:
            return [self._r.procedures[stripped.upper()]]

        words = {w for w in _tokens(text) if w not in _SIDE_WORDS}
        best: dict[str, int] = {}
        for p in self._r.procedures.values():
            for alias in [p.name, *p.aliases]:
                alias_words = set(_tokens(alias))
                if alias_words and alias_words <= words:
                    best[p.id] = max(best.get(p.id, 0), len(alias_words))
        if not best:
            return []
        top = max(best.values())
        return [self._r.procedures[pid] for pid, score in best.items() if score == top]

    def get_procedure(self, procedure_id: str) -> Procedure:
        if procedure_id not in self._r.procedures:
            raise NotFound("procedure", procedure_id)
        return self._r.procedures[procedure_id]

    # Patients and orders ----------------------------------------------------

    def find_patients(self, name: str, dob: date | None = None) -> list[Patient]:
        words = _tokens(name)
        if not words:
            return []
        found = [
            p
            for p in self._r.patients.values()
            if all(w in (p.first_name.lower(), p.last_name.lower()) for w in words)
        ]
        return [p for p in found if dob is None or p.dob == dob]

    def get_patient(self, mrn: str) -> Patient:
        if mrn not in self._r.patients:
            raise NotFound("patient", mrn)
        return self._r.patients[mrn]

    def orders_for_patient(self, mrn: str) -> list[SurgicalOrder]:
        return [o for o in self._r.orders if o.patient_mrn == mrn]

    def get_payer(self, payer_id: str) -> Payer:
        if payer_id not in self._r.payers:
            raise NotFound("payer", payer_id)
        return self._r.payers[payer_id]
