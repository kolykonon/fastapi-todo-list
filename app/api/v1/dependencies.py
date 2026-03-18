from typing import Annotated, Optional
from fastapi import status
from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from app.utils.jwt import decode_jwt
from app.core.security import validate_password
from app.core.db import SessionDep
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.repositories.auth_repository import AuthRepository

1
ouath2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/", scheme_name="JWT Authentication"
)


async def validate_auth_user(
    session: SessionDep, username: str = Form(), password: str = Form()
) -> User:
    unauthed_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Неправильный логин или пароль"
    )
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user: User = result.scalar_one_or_none()
    if not user:
        raise unauthed_exc
    print(user.password.encode("utf-8"))
    if not validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Пользователь неактивен")
    return user


async def get_current_token_payload(
    token: str = Depends(ouath2_scheme),
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")
    return payload


async def get_current_active_user(
    session: SessionDep,
    payload: dict = Depends(get_current_token_payload),
) -> User:
    id: str = payload.get("sub")
    query = select(User).where(User.id == int(id))
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный токен")
    return user


async def get_task_repository(session: SessionDep) -> TaskRepository:
    return TaskRepository(session)


async def get_auth_repository(session: SessionDep) -> AuthRepository:
    return AuthRepository(session)


UserValidateDep = Annotated[User, Depends(validate_auth_user)]

GetCurrentUserDep = Annotated[User, Depends(get_current_active_user)]

TaskRepositoryDep = Annotated[TaskRepository, Depends(get_task_repository)]

AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repository)]
