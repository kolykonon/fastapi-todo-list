from typing import Annotated
from pydantic import EmailStr
from schemas import CreateUserSchema, UserSchema, TokenSchema
from core import SessionDep
from models import User
from sqlalchemy import select
from fastapi import Depends, HTTPException, status, APIRouter, Form
from core.utils import hash_password, validate_password, encode_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(schema: CreateUserSchema, session: SessionDep):
    query = select(User).where(User.email == schema.email)
    user = await session.execute(query)
    if user.scalar_one_or_none():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Пользователь с таким email уже существует!"
        )
    else:
        hashed_password = hash_password(schema.password)
        user = User(email=schema.email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    return {"Ok": True}


async def validate_auth_user(
    session: SessionDep, email: EmailStr = Form(), password: str = Form()
) -> User:
    unauthed_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Неправильный логин или пароль"
    )
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user: User = result.scalar_one_or_none()
    if not user:
        raise unauthed_exc
    print(user.hashed_password.encode("utf-8"))
    if not validate_password(password=password, hashed_password=user.hashed_password):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Пользователь неактивен")
    return user


UserValidateDep = Annotated[User, Depends(validate_auth_user)]


@router.post("/login/")
async def auth_user(user: UserValidateDep):
    jwt_payload = {"sub": str(user.id), "email": user.email}
    token = encode_jwt(jwt_payload)
    return TokenSchema(access_token=token, token_type="Bearer")
