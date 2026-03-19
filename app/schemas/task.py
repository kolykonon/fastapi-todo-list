from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.task import TaskPriority, TaskStatus


class TaskSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreateSchema(TaskSchema):
    priority: TaskPriority

    @field_validator("due_date")
    def validate_due_to(cls, v: datetime) -> datetime:
        if v and v < datetime.now(timezone.utc):
            raise ValueError(
                "Срок выполнения задачи не может быть меньше, чем текущее время"
            )
        return v


class TaskUpdateSchema(TaskCreateSchema):
    status: TaskStatus


class TaskResponseSchema(TaskSchema):
    id: int
    priority: TaskPriority
    status: TaskStatus
    completed_at: Optional[datetime]
    user_id: int
    created_at: datetime
    updated_at: datetime

    @property
    def is_overdue(self) -> bool:
        if not self.due_date or self.is_completed:
            return False
        return datetime.now(timezone.utc) > self.due_date

    class Config:
        from_attributes = True
