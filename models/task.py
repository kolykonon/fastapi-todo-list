from sqlalchemy import String, Text
from typing import TYPE_CHECKING
from mixins import TimeStampMixin, IDMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base
from sqlalchemy import ForeignKey
import enum

if TYPE_CHECKING:
    from models import User


class TaskStatus(str, enum.Enum):
    """Класс статусов задач"""

    COMPLETED = "Completed"
    IN_PROGRESS = "In progress"
    CANCELED = "canceled"


class Task(Base, IDMixin, TimeStampMixin):
    """Класс, описывающий задачу в базе данных"""

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True, default="")
    status: Mapped[str] = mapped_column(
        String(20),
        default=TaskStatus.IN_PROGRESS,
        server_default=TaskStatus.IN_PROGRESS,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users: Mapped["User"] = relationship(back_populates="user")
