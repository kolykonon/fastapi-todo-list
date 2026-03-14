from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    email: EmailStr
    password: bytes
    is_active: bool = True
