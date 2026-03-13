from fastapi import APIRouter, HTTPException, status
from core import SessionDep
from sqlalchemy import Sequence, select
from models import Task
from schemas import TaskAddSchema, TaskSchema

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(session: SessionDep):
    """Функция для получения всех задач"""

    query = select(Task)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/")
async def add_task(schema: TaskAddSchema, session: SessionDep):
    """Функция для добавления задачи"""

    query = select(Task).where(schema.title == Task.title)
    task = await session.execute(query)
    if task.one_or_none():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Задача с таким названием уже существует!"
        )
    task = Task(**schema.model_dump())
    session.add(task)
    await session.commit()
    return task
