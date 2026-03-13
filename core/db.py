from config import db_settings
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DBHelper:
    def __init__(self):
        self.engine = create_async_engine(db_settings.get_db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )
