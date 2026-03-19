from typing import Annotated, Optional, Sequence
from fastapi import Depends, HTTPException
from app.core.exceptions import AlreadyExistsException, TaskNotFoundException
from app.repositories.task_repository import TaskRepositoryDep
from app.schemas.task import TaskResponseSchema, TaskSchema, TaskUpdateSchema
from app.models.task import Task
from app.schemas.task import TaskCreateSchema
from app.services.dependencies import GetCurrentUserDep
from app.utils.due_date import DueDate
from fastapi import status


class TaskService:
    """
    Класс реализующий бизнес-логику работы с задачами
    """

    def __init__(self, repository: TaskRepositoryDep, user: GetCurrentUserDep):
        self.repository = repository
        self.user = user

    async def get_all_tasks(self, status: Optional[str]) -> Optional[Sequence[Task]]:
        tasks = await self.repository.get_tasks(user_id=self.user.id, status=status)
        if tasks:
            return tasks
        else:
            return {"msg": "Задачи не найдены, хотите добавить?"}

    async def create_new_task(self, data: TaskCreateSchema) -> Task:
        task = await self.repository.get_task_by_title(
            task_title=data.title, user_id=self.user.id
        )
        if task:
            raise AlreadyExistsException(Task)
        try:
            due_date = DueDate(data.due_date)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Ошибка: {e}"
            )
        data.due_date = due_date.value
        return await self.repository.add_task(data=data, user_id=self.user.id)

    async def get_one_task(self, task_id: int) -> TaskResponseSchema:
        task = await self.repository.get_task_by_id(
            task_id=task_id, user_id=self.user.id
        )
        if not task:
            raise TaskNotFoundException
        return task

    async def get_active_tasks(self) -> Sequence[Task]:
        return await self.repository.get_active_tasks(user_id=self.user.id)

    async def delete_task(self, task_id: int) -> TaskSchema:
        task = await self.repository.get_task_by_id(
            task_id=task_id, user_id=self.user.id
        )
        if not task:
            raise TaskNotFoundException
        return await self.repository.delete_task_by_id(
            task_id=task_id, user_id=self.user.id
        )

    async def update_task(self, data: TaskUpdateSchema, task_id: int) -> Task:
        task = await self.repository.get_task_by_id(
            task_id=task_id, user_id=self.user.id
        )
        if not task:
            raise TaskNotFoundException
        task = await self.repository.update_task(task=task, schema=data)
        return task


def get_task_service(repository: TaskRepositoryDep, user: GetCurrentUserDep):
    return TaskService(repository, user)


TaskService = Annotated[TaskService, Depends(get_task_service)]
