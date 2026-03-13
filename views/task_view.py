from fastapi import APIRouter
from core import SessionDep
from sqlalchemy import select
from models import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_tasks(session: SessionDep):
    """Функция для получения всех заданий"""

    query = select(Task)
    result = await session.execute(query)
    return result.scalars().all()
