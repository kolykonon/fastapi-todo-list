from typing import Annotated
from alembic.util import status
from fastapi import Depends, Form, HTTPException
from sqlalchemy import select
from core.security import validate_password
from core.db import SessionDep
from models.user import User


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


UserValidateDep = Annotated[User, Depends(validate_auth_user)]
