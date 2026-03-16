from pydantic import BaseModel, ConfigDict, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    password: str
    is_active: bool = True
