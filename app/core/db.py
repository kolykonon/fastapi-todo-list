from typing import Annotated, AsyncGenerator
from fastapi import Depends
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class DBHelper:
    """Класс для удобной работы с сессиями бд"""

    def __init__(self):
        self.engine = create_async_engine(settings.db_settings.get_db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def get_session(
        self,
    ) -> AsyncGenerator[AsyncSession]:  # Функция для проброса сессии
        async with self.session_factory.begin() as session:
            yield session


db_helper = DBHelper()
SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
