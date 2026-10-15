"""In-memory Store for tests and single-process demos.

Records are kept as JSON, exactly as the SQLite adapter will keep them, so anything
that doesn't round-trip fails here first.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class MemoryStore:
    def __init__(self) -> None:
        self._data: dict[str, dict[str, str]] = {}

    def save(self, collection: str, key: str, record: BaseModel) -> None:
        self._data.setdefault(collection, {})[key] = record.model_dump_json()

    def load(self, collection: str, key: str, model: type[T]) -> T | None:
        raw = self._data.get(collection, {}).get(key)
        return model.model_validate_json(raw) if raw is not None else None

    def list(self, collection: str, model: type[T]) -> list[T]:
        return [model.model_validate_json(raw) for raw in self._data.get(collection, {}).values()]

    def delete(self, collection: str, key: str) -> None:
        self._data.get(collection, {}).pop(key, None)
