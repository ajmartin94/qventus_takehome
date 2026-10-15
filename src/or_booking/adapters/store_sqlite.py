"""SQLite Store: requests and sessions survive a restart, so a reply hours later finds its draft.

One table of JSON documents keyed by (collection, key). Production would use the
hospital's or Qventus's database behind the same port.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SqliteStore:
    def __init__(self, path: Path) -> None:
        if str(path) != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(path))
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS records (collection TEXT, key TEXT, body TEXT, PRIMARY KEY (collection, key))"
        )

    def save(self, collection: str, key: str, record: BaseModel) -> None:
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO records (collection, key, body) VALUES (?, ?, ?)",
                (collection, key, record.model_dump_json()),
            )

    def load(self, collection: str, key: str, model: type[T]) -> T | None:
        row = self._db.execute("SELECT body FROM records WHERE collection = ? AND key = ?", (collection, key)).fetchone()
        return model.model_validate_json(row[0]) if row else None

    def list(self, collection: str, model: type[T]) -> list[T]:
        rows = self._db.execute("SELECT body FROM records WHERE collection = ? ORDER BY rowid", (collection,)).fetchall()
        return [model.model_validate_json(body) for (body,) in rows]

    def delete(self, collection: str, key: str) -> None:
        with self._db:
            self._db.execute("DELETE FROM records WHERE collection = ? AND key = ?", (collection, key))
