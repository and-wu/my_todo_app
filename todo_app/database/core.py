import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


class DataBase:
    def __init__(self, path: str) -> None:
        self.path = path

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor]:
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            conn.close()

    def create_tasks_table(self) -> None:
        with self.get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    priority INTEGER NOT NULL DEFAULT 1
                )
            """)

def get_database(path: Path) -> DataBase:
    return DataBase(path.as_posix())
