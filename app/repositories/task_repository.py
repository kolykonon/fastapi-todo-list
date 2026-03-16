from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import TaskAddSchema
from models.task import Task
from typing import Optional, Sequence


class TaskRepository:

    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_tasks(
        self, user_id: int, status: Optional[str] = None
    ) -> Optional[Sequence[Task]]:
        query = select(Task).where(Task.user_id == user_id)
        if status:
            query = query.where(Task.status == status)
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()
        return task

    async def add_task(self, task_data: TaskAddSchema, user_id: int) -> Optional[Task]:
        new_task = Task(**task_data.model_dump(), user_id=user_id)
        self.session.add(new_task)
        await self.session.commit()
        return new_task

    async def get_task_by_title(self, task_title: str, user_id: int):
        query = select(Task).where(Task.title == task_title, Task.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
