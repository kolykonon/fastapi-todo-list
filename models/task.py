from sqlalchemy import String, Text
from mixins import TimeStampMixin, IDMixin
from sqlalchemy.orm import Mapped, mapped_column
from models import Base
import enum


class TaskStatus(str, enum.Enum):
    """Класс статусов задач"""

    COMPLETED = "Completed"
    IN_PROGRESS = "In progress"
    CANCELED = "canceled"


class Task(Base, IDMixin, TimeStampMixin):
    """Класс, описывающий задачу в базе данных"""

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text(500), nullable=True, default="")
    status: Mapped[str] = mapped_column(
        String(20),
        default=TaskStatus.IN_PROGRESS,
        server_default=TaskStatus.IN_PROGRESS,
    )
