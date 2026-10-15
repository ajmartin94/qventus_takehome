"""Loads the simulated hospital's EHR files into domain models.

Shared by the fixture directory and the mock scheduling service, which in a real
hospital would each read the same EHR and credentialing data. Every file is validated
on load, and cross-references are checked, so a malformed record fails at startup.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, TypeAdapter, ValidationError

from or_booking.domain.models import Patient, Payer, Procedure, Surgeon, SurgicalOrder

T = TypeVar("T", bound=BaseModel)


class FixtureError(ValueError):
    """A fixture file is malformed or refers to something that doesn't exist."""


def read_yaml(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError as err:
        raise FixtureError(f"missing fixture file {path}") from err


def parse(path: Path, data: Any, model: type[T]) -> T:
    try:
        return model.model_validate(data)
    except ValidationError as err:
        raise FixtureError(f"{path}: {err}") from err


def parse_list(path: Path, model: type[T]) -> list[T]:
    try:
        return TypeAdapter(list[model]).validate_python(read_yaml(path))  # type: ignore[valid-type]
    except ValidationError as err:
        raise FixtureError(f"{path}: {err}") from err


@dataclass(frozen=True)
class EhrRecords:
    surgeons: dict[str, Surgeon]
    procedures: dict[str, Procedure]
    patients: dict[str, Patient]
    orders: list[SurgicalOrder]
    payers: dict[str, Payer]


def load_ehr(fixtures_dir: Path) -> EhrRecords:
    ehr = fixtures_dir / "ehr"
    records = EhrRecords(
        surgeons={s.id: s for s in parse_list(ehr / "surgeons.yaml", Surgeon)},
        procedures={p.id: p for p in parse_list(ehr / "procedures.yaml", Procedure)},
        patients={p.mrn: p for p in parse_list(ehr / "patients.yaml", Patient)},
        orders=parse_list(ehr / "orders.yaml", SurgicalOrder),
        payers={p.id: p for p in parse_list(ehr / "payers.yaml", Payer)},
    )
    _check_references(records)
    return records


def _check_references(r: EhrRecords) -> None:
    problems: list[str] = []
    for s in r.surgeons.values():
        problems += [f"surgeon {s.id} privileged for unknown procedure {p}" for p in s.privileges if p not in r.procedures]
    for p in r.patients.values():
        if p.payer_id and p.payer_id not in r.payers:
            problems.append(f"patient {p.mrn} has unknown payer {p.payer_id}")
    for o in r.orders:
        if o.patient_mrn not in r.patients:
            problems.append(f"order {o.id} for unknown patient {o.patient_mrn}")
        if o.surgeon_id not in r.surgeons:
            problems.append(f"order {o.id} by unknown surgeon {o.surgeon_id}")
        procedure = r.procedures.get(o.procedure_id)
        if procedure is None:
            problems.append(f"order {o.id} for unknown procedure {o.procedure_id}")
        elif (procedure.laterality == "required") != (o.laterality is not None):
            problems.append(f"order {o.id}: laterality must be stated exactly when {o.procedure_id} has one")
        if o.surgeon_id in r.surgeons and o.procedure_id not in r.surgeons[o.surgeon_id].privileges:
            problems.append(f"order {o.id}: {o.surgeon_id} is not privileged for {o.procedure_id}")
    if problems:
        raise FixtureError("EHR fixtures are inconsistent:\n  " + "\n  ".join(problems))
