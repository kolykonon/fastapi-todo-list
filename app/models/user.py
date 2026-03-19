from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from app.models import Base
from app.models.mixins import IDMixin, TimeStampMixin

if TYPE_CHECKING:  # Чтобы избежать циклического импорта
    from app.models import Task


class User(Base, IDMixin, TimeStampMixin):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")
    is_active: Mapped[bool] = mapped_column(default=True)
