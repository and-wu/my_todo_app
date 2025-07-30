from todo_app.models import TodoItem, CreatTodoItemSchema, ReadTodoItemSchema, ChangeSchema
from todo_app.database.core import DataBase
from todo_app.database.repository.base import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, database: DataBase):
        super().__init__(database, table="tasks")

    @staticmethod
    def _row_to_todo(row):
        return TodoItem(id=row[0],
                        title=row[1],
                        description=row[2],
                        completed=bool(row[3]),
                        created_at=row[4],
                        priority=(row[5])
        )

    def all_tasks(self):
        rows = self.get_all()
        return [ReadTodoItemSchema(id=row[0],
                                   title=row[1],
                                   description=row[2],
                                   completed=bool(row[3]),
                                   created_at=row[4],
                                   priority = row[5]) for row in rows]

    def get_task(self, task_id: int):
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def create_task(self, data: CreatTodoItemSchema):
        task_id = self.create(data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def update_task(self, task_id: int, data: CreatTodoItemSchema):
        self.update(task_id, data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def change_task(self, task_id: int, data: ChangeSchema ):
        self.change(task_id, data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def change_completed(self, task_id: int):
        task = self.get_task(task_id)
        new_completed = not task.completed

        with self.db.get_cursor() as cursor:
            cursor.execute(f"UPDATE {self.table} SET completed = ? WHERE id = ?", (int(new_completed), task_id))

        return TodoItem(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=new_completed,
            created_at=task.created_at,
            priority=task.priority
        )

    def delete_task(self, task_id: int):
        self.delete(task_id)

