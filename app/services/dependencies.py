from typing import Annotated
from alembic.util import status
from fastapi import Depends, Form, HTTPException
from app.core.exceptions import UnauthorizedException
from app.core.security import validate_password
from app.models.user import User
from app.repositories.auth_repository import AuthRepositoryDep
from app.services.token_service import get_current_token_payload


async def validate_auth_user(
    repository: AuthRepositoryDep, username: str = Form(), password: str = Form()
) -> User:
    user = await repository.get_user_by_name(username=username)
    if not user:
        raise UnauthorizedException

    if not validate_password(password=password, hashed_password=user.password):
        raise UnauthorizedException

    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Пользователь неактивен")
    return user


async def get_current_active_user(
    repository: AuthRepositoryDep,
    payload: dict = Depends(get_current_token_payload),
) -> User:
    username: str = payload.get("username")
    user = await repository.get_user_by_name(username=username)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Невалидныйz токен")
    return user


ValidateUserDep = Annotated[User, Depends(validate_auth_user)]
GetCurrentUserDep = Annotated[User, Depends(get_current_active_user)]
