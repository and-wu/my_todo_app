from pydantic import BaseModel
from ..core import DataBase


class BaseRepository:
    def __init__(self, database: DataBase, table: str):
        self.db = database
        self.table = table

    def create(self, data: BaseModel):
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            raise ValueError("Нет данных для создания.")

        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        values = list(fields.values())

        with self.db.get_cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})",
                values
            )
            row_id = cursor.lastrowid
            return row_id

    def update(self, row_id: int, data: BaseModel):
        fields = data.model_dump(exclude_unset=True)
        if not fields:
            raise ValueError("Нет данных для обновления.")

        updates = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values())

        with self.db.get_cursor() as cursor:
            cursor.execute(
                f"UPDATE {self.table} SET {updates} WHERE id = ?",
                (*values, row_id)
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Запись с id={row_id} не найдена.")
            return True



    def delete(self, row_id: int):
        with self.db.get_cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.table} WHERE id = ?", (row_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Запись с id={row_id} не найдена.")

    def get_by_id(self, row_id: int):
        with self.db.get_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = ?", (row_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"Запись с id={row_id} не найдена.")
            return row

    def get_all(self):
        with self.db.get_cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table}")
            return cursor.fetchall()
