import aiosqlite
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path


class DataBase:
    def __init__(self, path: str) -> None:
        self.path = path

    @asynccontextmanager
    async def get_cursor(self) -> AsyncGenerator[aiosqlite.Cursor]:
        conn = await aiosqlite.connect(self.path)
        try:
            cursor = await conn.cursor()
            yield cursor
            await conn.commit()
        finally:
            await conn.close()


    async def create_tasks_table(self) -> None:
        async with self.get_cursor() as cursor:
            await cursor.execute("""
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
