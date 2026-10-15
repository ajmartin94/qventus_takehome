"""Store port: persists requests, drafts and sessions across channels and hours.

A question asked by fax may be answered hours later, so session state outlives a
conversation. Records are Pydantic models stored as JSON, so every adapter (in-memory
or SQLite) round-trips them the same way.
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@runtime_checkable
class Store(Protocol):
    def save(self, collection: str, key: str, record: BaseModel) -> None: ...

    def load(self, collection: str, key: str, model: type[T]) -> T | None: ...

    def list(self, collection: str, model: type[T]) -> list[T]: ...

    def delete(self, collection: str, key: str) -> None: ...
