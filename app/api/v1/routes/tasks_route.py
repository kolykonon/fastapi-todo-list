from typing import List, Optional
from fastapi import APIRouter
from app.schemas.task import (
    TaskResponseSchema,
    TaskCreateSchema,
    TaskUpdateSchema,
)
from app.services.tasks_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskResponseSchema])
async def get_tasks(service: TaskService, status: Optional[str] = None):
    return await service.get_all_tasks(status=status)


@router.post("/", response_model=TaskResponseSchema)
async def create_task(
    schema: TaskCreateSchema,
    service: TaskService,
):
    return await service.create_new_task(data=schema)


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_one_task(task_id: int, service: TaskService):
    task = await service.get_one_task(task_id=task_id)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task_by_id(task_id: int, service: TaskService) -> None:
    await service.delete_task(task_id=task_id)
    return None


@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: int,
    schema: TaskUpdateSchema,
    service: TaskService,
):
    return await service.update_task(data=schema, task_id=task_id)


@router.get("/tasks/active", response_model=List[TaskResponseSchema])
async def get_active_tasks(service: TaskService):
    return await service.get_active_tasks()
