from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from models import Base
from mixins import IDMixin, TimeStampMixin
from pydantic import EmailStr

if TYPE_CHECKING:  # Чтобы избежать циклического импорта
    from models import Task


class User(Base, IDMixin, TimeStampMixin):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="user")
    is_active: Mapped[bool] = mapped_column(default=True)
