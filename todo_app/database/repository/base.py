from pydantic import BaseModel
from ..core import DataBase

class BaseRepository:
    def __init__(self, database: DataBase, table: str) -> None:
        self.db = database
        self.table = table

    async def create(self, data: BaseModel) -> int:
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            raise ValueError("Нет данных для создания.")

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        values = list(fields.values())

        async with self.db.get_cursor() as cursor:
            await cursor.execute(
                f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})",
                values
            )
            row_id = cursor.lastrowid
            return row_id

    async def update(self, row_id: int, data: BaseModel) -> bool:
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            raise ValueError("Нет данных для обновления.")

        updates = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values())

        async with self.db.get_cursor() as cursor:
            await cursor.execute(
                f"UPDATE {self.table} SET {updates} WHERE id = ?",
                (*values, row_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Запись с id={row_id} не найдена.")
            return True

    async def change(self, row_id: int, data: BaseModel) -> bool:
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            raise ValueError("Нет данных для обновления.")

        columns = ", ".join(f"{key} = ?" for key in fields.keys())
        values = list(fields.values())

        async with self.db.get_cursor() as cursor:
            await cursor.execute(
                f"UPDATE {self.table} SET {columns} WHERE id = ?",
                (*values, row_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Задача с id={row_id} не найдена.")
        return True


    async def delete(self, row_id: int) -> None:
        async with self.db.get_cursor() as cursor:
            await cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (row_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Запись с id={row_id} не найдена.")

    async def get_by_id(self, row_id: int) -> tuple:
        async with self.db.get_cursor() as cursor:
            await cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (row_id,))
            row = await cursor.fetchone()
            if row is None:
                raise ValueError(f"Запись с id={row_id} не найдена.")
            return row

    async def get_all(self) -> list:
        async with self.db.get_cursor() as cursor:
            await cursor.execute(f"SELECT * FROM {self.table}")
            return await cursor.fetchall()
