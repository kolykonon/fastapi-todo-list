from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import TaskAddSchema
from models.task import Task
from typing import Optional, Sequence


class TaskRepository:
    def __init__(self, session):
        self.session: AsyncSession
        self.user_id: int

    async def get_tasks(self, status: Optional[str] = None) -> Optional[Sequence[Task]]:
        query = select(Task).where(Task.user_id == self.user_id)
        if status:
            query = query.where(status=status)
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        query = select(Task).where(Task.id == task_id, Task.user_id == self.user_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()
        return task

    async def add_task(self, task_data: TaskAddSchema) -> Optional[Task]:
        new_task = Task(**task_data.model_dump(), user_id=self.user_id)
        self.session.add(new_task)
        await self.session.commit()
        return new_task
