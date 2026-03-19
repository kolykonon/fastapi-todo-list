from datetime import datetime, timezone
from app.models.task import TaskStatus
from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import SessionDep
from app.schemas.task import TaskCreateSchema, TaskSchema
from app.models.task import Task
from typing import Annotated, Optional, Sequence


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

    async def add_task(self, data: TaskCreateSchema, user_id: int) -> Optional[Task]:
        new_task = Task(
            title=data.title,
            description=data.description,
            status="В работе",
            due_date=data.due_date,
            completed_at=None,
            priority=data.priority,
            user_id=user_id,
        )
        self.session.add(new_task)
        await self.session.commit()
        return new_task

    async def get_task_by_title(self, task_title: str, user_id: int) -> Optional[Task]:
        query = select(Task).where(Task.title == task_title, Task.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_task_by_id(self, task_id: int, user_id: int) -> dict:
        query = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
        await self.session.execute(query)
        await self.session.commit()

    async def update_task(self, task: Task, schema: TaskSchema) -> TaskSchema:
        update_data = schema.model_dump(exclude_none=True)

        for key, value in update_data.items():
            setattr(task, key, value)

        await self.session.commit()

        return TaskSchema.model_validate(task, from_attributes=True)

    async def get_active_tasks(self, user_id: int) -> Optional[Sequence[Task]]:
        query = select(Task).where(
            Task.status == TaskStatus.IN_PROGRESS,
            Task.due_date > datetime.now(timezone.utc),
            Task.user_id == user_id,
        )
        active_tasks = await self.session.execute(query)
        active_tasks = active_tasks.scalars().all()
        return active_tasks


async def get_task_repository(session: SessionDep) -> TaskRepository:
    return TaskRepository(session)


TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]
