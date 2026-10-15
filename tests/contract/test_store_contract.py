"""Store contract: what the orchestrator relies on, for every adapter (in-memory and SQLite)."""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from or_booking.adapters.store_memory import MemoryStore
from or_booking.adapters.store_sqlite import SqliteStore
from or_booking.ports.store import Store


class Note(BaseModel):
    text: str
    count: int = 0


@pytest.fixture(params=["memory", "sqlite"])
def store(request: pytest.FixtureRequest, tmp_path) -> Store:
    return MemoryStore() if request.param == "memory" else SqliteStore(tmp_path / "store.sqlite3")


def test_records_round_trip_and_replace(store: Store) -> None:
    store.save("notes", "a", Note(text="first"))
    store.save("notes", "a", Note(text="second", count=2))
    assert store.load("notes", "a", Note) == Note(text="second", count=2)
    assert store.load("notes", "missing", Note) is None


def test_collections_are_separate_and_listable(store: Store) -> None:
    store.save("notes", "a", Note(text="a"))
    store.save("notes", "b", Note(text="b"))
    store.save("other", "a", Note(text="x"))
    assert sorted(n.text for n in store.list("notes", Note)) == ["a", "b"]
    store.delete("notes", "a")
    assert [n.text for n in store.list("notes", Note)] == ["b"]


def test_sqlite_survives_a_restart(tmp_path) -> None:
    SqliteStore(tmp_path / "s.sqlite3").save("notes", "a", Note(text="kept"))
    assert SqliteStore(tmp_path / "s.sqlite3").load("notes", "a", Note) == Note(text="kept")
