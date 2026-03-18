from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator
import re
import string


class CreateUserSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    password: SecretStr = Field(min_length=8)
    is_active: bool = True

    @field_validator("password")
    def validate_password(cls, v: str):
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r'[!@#$^&*(),.?":{}|<>_]', v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return v
