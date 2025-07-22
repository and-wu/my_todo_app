from pydantic import BaseModel
from datetime import datetime

class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime

class CreatTodoItemSchema(BaseModel):
    title: str
    description: str
    completed: bool = False

class ReadTodoItemSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime