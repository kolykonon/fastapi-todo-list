from datetime import datetime
from sqlalchemy import DateTime, String, Text
from typing import TYPE_CHECKING
from app.models.mixins import TimeStampMixin, IDMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import Base
from sqlalchemy import ForeignKey
import enum

if TYPE_CHECKING:
    from models import User


class TaskPriority(str, enum.Enum):
    """
    Класс приоритетов задач

    """

    HIGH = "Высокий"
    MED = "Средний"
    LOW = "Низкий"


class TaskStatus(str, enum.Enum):
    """Класс статусов задач"""

    COMPLETED = "Завершена"
    IN_PROGRESS = "В работе"
    CANCELED = "Отменена"


class Task(Base, IDMixin, TimeStampMixin):
    """
    Класс, описывающий задачу в базе данных
    """

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True, default="")
    status: Mapped[str] = mapped_column(
        String(20),
        default=TaskStatus.IN_PROGRESS,
        server_default=TaskStatus.IN_PROGRESS,
    )
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    priority: Mapped[str] = mapped_column(
        String(10), default=TaskPriority.MED, server_default=TaskPriority.MED
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="tasks")
