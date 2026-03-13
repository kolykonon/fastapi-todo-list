from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime


class TimeStampMixin:
    """Миксин для добавления полей создания и обновления таблицы"""

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )
