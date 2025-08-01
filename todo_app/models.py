from pydantic import BaseModel
from datetime import datetime
from .enums import Priority

class ChangeSchema(BaseModel):
    completed: bool | None = None
    priority: Priority | None = None


class TodoItem(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime
    priority: Priority

class CreatTodoItemSchema(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: Priority = Priority.LOW

class ReadTodoItemSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime
    priority: Priority
