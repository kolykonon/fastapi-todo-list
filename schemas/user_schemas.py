from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
