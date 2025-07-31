from todo_app.models import TodoItem, CreatTodoItemSchema
from todo_app.models import ReadTodoItemSchema, ChangeSchema
from todo_app.database.core import DataBase
from todo_app.database.repository.base import BaseRepository

class TaskRepository(BaseRepository):
    def __init__(self, database: DataBase) -> None:
        super().__init__(database, table="tasks")

    @staticmethod
    def _row_to_todo(row: tuple) -> TodoItem:
        return TodoItem(id=row[0],
                        title=row[1],
                        description=row[2],
                        completed=bool(row[3]),
                        created_at=row[4],
                        priority=(row[5])
        )

    def all_tasks(self) -> list[ReadTodoItemSchema]:
        rows = self.get_all()
        return [ReadTodoItemSchema(id=row[0],
                                   title=row[1],
                                   description=row[2],
                                   completed=bool(row[3]),
                                   created_at=row[4],
                                   priority = row[5]) for row in rows]

    def get_task(self, task_id: int) -> TodoItem:
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def create_task(self, data: CreatTodoItemSchema) -> TodoItem:
        task_id = self.create(data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def update_task(self, task_id: int, data: CreatTodoItemSchema) -> TodoItem:
        self.update(task_id, data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def change_task(self, task_id: int, data: ChangeSchema) -> TodoItem:
        self.change(task_id, data)
        row = self.get_by_id(task_id)
        return self._row_to_todo(row=row)

    def delete_task(self, task_id: int) -> None:
        self.delete(task_id)
