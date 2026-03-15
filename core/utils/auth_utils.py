from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.db import SessionDep
from schemas import UserSchema
from core.utils import decode_jwt
from sqlalchemy import select
from models import User
from jwt.exceptions import InvalidTokenError

ouath2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/", scheme_name="JWT Authentication"
)


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
