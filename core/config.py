from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class DBSettings(BaseSettings):
    """Класс настроек базы данных"""

    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def get_db_url(self) -> str:  # Возвращает URL базы данных
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_settings = DBSettings()
