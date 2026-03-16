from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass

    @declared_attr
    def __tablename__(cls) -> str:  # Название таблицы в постгресе = Название класса + s
        return cls.__name__.lower() + "s"
