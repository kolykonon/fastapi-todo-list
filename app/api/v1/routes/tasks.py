from typing import Optional
from fastapi import APIRouter
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

    task = await repo.get_task_by_title(task_title=schema.title, user_id=user.id)
    if task:
        raise TaskAlreadyExistsException
    return await repo.add_task(task_data=schema, user_id=user.id)


@router.get("/{task_id}", response_model=TaskSchema)
async def get_one_task(
    task_id: int, user: GetCurrentUserDep, repo: TaskRepositoryDep
) -> TaskSchema:
    task = await repo.get_task_by_id(task_id=task_id, user_id=user.id)
    if task:
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
    task_id: int, user: GetCurrentUserDep, repo: TaskRepositoryDep
) -> dict:
    task = await repo.get_task_by_id(task_id=task_id, user_id=user.id)
    if task:
        deleted = await repo.delete_task_by_id(task_id=task_id, user_id=user.id)
        return deleted
    else:
        raise TaskNotFoundException


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    schema: TaskAddSchema,
    user: GetCurrentUserDep,
    repo: TaskRepositoryDep,
):
    task = await repo.get_task_by_id(task_id=task_id, user_id=user.id)
    if task:
        task = await repo.update_task(task=task, schema=schema)
        return task
    raise TaskNotFoundException
