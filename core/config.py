from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


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


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    """Общий класс настроек"""

    db_settings: DBSettings = DBSettings()
    jwt_settings: AuthJWT = AuthJWT()


settings = Settings()
