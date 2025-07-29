from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from .enums import Priority

class PriorityChangeSchema(BaseModel):
    priority: int


class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    priority: Priority

class CreatTodoItemSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Priority = Priority.LOW

class ReadTodoItemSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    priority: Priority