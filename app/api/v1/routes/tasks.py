from fastapi import APIRouter
from core.db import SessionDep
from sqlalchemy import select, delete, update
from models.task import Task
from schemas.task import TaskAddSchema, TaskSchema
from api.v1.exceptions import TaskNotFoundException, TaskAlreadyExistsException

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(session: SessionDep):
    """Функция для получения всех задач"""

    query = select(Task)
    result = await session.execute(query)
    tasks = result.scalars().all()
    if tasks:
        return tasks
    else:
        return {"msg": "Задачи не найдены!"}


@router.post("/")
async def add_task(schema: TaskAddSchema, session: SessionDep):
    """Функция для добавления задачи"""

    query = select(Task).where(schema.title == Task.title)
    task = await session.execute(query)
    if task.one_or_none():
        raise TaskAlreadyExistsException
    task = Task(**schema.model_dump())
    session.add(task)
    await session.commit()
    return task


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task_by_id(task_id: int, session: SessionDep) -> TaskSchema:
    result = await session.get(Task, 1)
    if result:
        return TaskSchema(
            id=result.id,
            title=result.title,
            description=result.description,
            status=result.status,
        )
    else:
        raise TaskNotFoundException


@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, session: SessionDep) -> dict:
    task = await session.get(Task, task_id)
    if task:
        await session.execute(delete(Task).where(Task.id == task_id))
        await session.commit()
        return {"status": "Задача удалена"}
    else:
        raise TaskNotFoundException


@router.put("/{task_id}")
async def update_task(task_id: int, schema: TaskAddSchema, session: SessionDep):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.one_or_none()
    if not task:
        raise TaskNotFoundException
    update_data = TaskAddSchema.model_dump(exclude_none=True)
    for key, value in update_data:
        setattr(task, key, value)
    session.refresh(task)
    await session.commit()
