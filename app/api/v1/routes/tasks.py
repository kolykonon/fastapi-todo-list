from fastapi import APIRouter
from core.db import SessionDep
from sqlalchemy import select, delete
from models.task import Task
from schemas.task import TaskAddSchema, TaskSchema
from api.v1.exceptions import TaskNotFoundException, TaskAlreadyExistsException
from api.v1.dependencies import GetCurrentUserDep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(session: SessionDep, user: GetCurrentUserDep):
    """Функция для получения всех задач"""

    query = select(Task).where(Task.user_id == user.id)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if tasks:
        return tasks
    else:
        return {"msg": "Задачи не найдены!"}


@router.post("/")
async def add_task(schema: TaskAddSchema, session: SessionDep, user: GetCurrentUserDep):
    """Функция для добавления задачи"""

    query = select(Task).where(schema.title == Task.title, Task.user_id == user.id)
    task = await session.execute(query)
    if task.one_or_none():
        raise TaskAlreadyExistsException
    task = Task(**schema.model_dump(), user_id=user.id)
    session.add(task)
    await session.commit()
    return task


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task_by_id(
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
