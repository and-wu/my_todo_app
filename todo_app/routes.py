from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from typing import List

from todo_app.database.repository.tasks import TaskRepository
from .models import TodoItem, CreatTodoItemSchema, ReadTodoItemSchema, PriorityChangeSchema

router = APIRouter()

def get_crud(request: Request):
    return request.app.state.crud

@router.get('/')
def hello_todo():
    return {
        'message': 'hello, this is my ToDo with DateBase'
    }

@router.get('/todos', response_model=List[ReadTodoItemSchema])
def get_list_tasks(crud: TaskRepository = Depends(get_crud)):
    return crud.all_tasks()

@router.post('/todos', response_model=TodoItem)
def creat_task(task: CreatTodoItemSchema, crud: TaskRepository = Depends(get_crud)):
    new_task = crud.create_task(task)
    return new_task

@router.put("/todos/{id}", response_model=TodoItem)
def update_task(id: int, updated_task: CreatTodoItemSchema, crud: TaskRepository = Depends(get_crud)):
    new_task = crud.update_task(task_id=id, data=updated_task)
    return new_task

@router.patch("/todos/{id}/change-completed")
def change_completed(id: int, crud: TaskRepository = Depends(get_crud)):
    try:
        new_task = crud.change_completed(id)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при удалении задачи")

@router.patch("/todos/{id}/change-priority", response_model=TodoItem)
def change_priority(id: int, data: PriorityChangeSchema, crud: TaskRepository = Depends(get_crud)):
    try:
        new_task = crud.change_priority(id, data.priority)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при изменении приоритета задачи")

@router.delete('/todos/{id}')
def delete_task(id: int, crud: TaskRepository = Depends(get_crud)):
    try:
        crud.delete_task(id)
        return True
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при удалении задачи")