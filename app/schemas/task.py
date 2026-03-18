from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import TaskStatus


class TaskAddSchema(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: Optional[str]
    status: TaskStatus


class TaskSchema(TaskAddSchema):
    id: int
