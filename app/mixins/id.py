from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    """Миксин для добавления поля id в таблицу"""

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
