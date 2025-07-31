from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from todo_app.database.repository.tasks import TaskRepository
from todo_app.routes import router
from todo_app.database.core import get_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    db = get_database(Path('todos.db'))
    db.create_tasks_table()
    app.state.crud = TaskRepository(database=db)
    yield

app = FastAPI(lifespan=lifespan, title="ToDo API with DB")

# CORS (разрешаем доступ с любого домена)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
