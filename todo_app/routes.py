from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request

from todo_app.database.repository.tasks import TaskRepository
from .models import TodoItem, CreatTodoItemSchema, ReadTodoItemSchema, ChangeSchema
router = APIRouter()

def get_crud(request: Request) -> TaskRepository:
    return request.app.state.crud

@router.get('/')
def hello_todo() -> dict:
    return {
        'message': 'hello, this is my ToDo with DateBase'
    }

@router.get('/todos', response_model=list[ReadTodoItemSchema])
async def get_list_tasks(crud: TaskRepository = Depends(get_crud)) -> list[tuple]:
    return await crud.all_tasks()

@router.post('/todos', response_model=TodoItem)
async def creat_task(task: CreatTodoItemSchema,
               crud: TaskRepository = Depends(get_crud)) -> TodoItem:
    return await crud.create_task(task)

@router.put("/todos/{id}", response_model=TodoItem)
async def update_task(id: int,
                updated_task: CreatTodoItemSchema,
                crud: TaskRepository = Depends(get_crud)) -> TodoItem:
    return await crud.update_task(task_id=id, data=updated_task)

@router.patch("/todos/{id}")
async def change_task(id: int,
                change_data: ChangeSchema,
                crud: TaskRepository = Depends(get_crud)) -> TodoItem:
    try:
        return await crud.change_task(task_id=id, data=change_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении задачи")


@router.delete('/todos/{id}')
async def delete_task(id: int, crud: TaskRepository = Depends(get_crud)) -> None:
    try:
        await crud.delete_task(id)
        return True
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при удалении задачи")
