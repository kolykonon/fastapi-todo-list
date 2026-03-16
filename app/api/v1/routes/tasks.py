from typing import Optional
from fastapi import APIRouter
from core.db import SessionDep
from sqlalchemy import select, delete
from models.task import Task
from schemas.task import TaskAddSchema, TaskSchema
from api.v1.exceptions import TaskNotFoundException, TaskAlreadyExistsException
from api.v1.dependencies import GetCurrentUserDep, TaskRepositoryDep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(
    user: GetCurrentUserDep, repo: TaskRepositoryDep, status: Optional[str] = None
):
    """Функция для получения всех задач"""
    tasks = await repo.get_tasks(status=status, user_id=user.id)
    if tasks:
        return tasks
    else:
        return {"msg": "Задачи не найдены!"}


@router.post("/")
async def create_task(
    schema: TaskAddSchema,
    user: GetCurrentUserDep,
    repo: TaskRepositoryDep,
):
    """Функция для добавления задачи"""

    task = repo.get_task_by_id()
    if task.one_or_none():
        raise TaskAlreadyExistsException
    return repo.add_task(task_data=schema, user_id=user.id)


@router.get("/{task_id}", response_model=TaskSchema)
async def get_one_task(
    task_id: int, session: SessionDep, user: GetCurrentUserDep
) -> TaskSchema:
    query = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if result:
        return TaskSchema(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
        )
    else:
        raise TaskNotFoundException


@router.delete("/{task_id}")
async def delete_task_by_id(
    task_id: int, session: SessionDep, user: GetCurrentUserDep
) -> dict:
    task = await session.get(Task, task_id)
    if task:
        await session.execute(delete(Task).where(Task.id == task_id))
        await session.commit()
        return {"status": "Задача удалена"}
    else:
        raise TaskNotFoundException


@router.put("/{task_id}")
async def update_task(
    task_id: int, schema: TaskAddSchema, session: SessionDep, user: GetCurrentUserDep
):
    query = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()
    if task:
        update_data = schema.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        await session.commit()

        return TaskSchema.model_validate(task, from_attributes=True)
    raise TaskNotFoundException
