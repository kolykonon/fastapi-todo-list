from fastapi import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.utils.jwt import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login", scheme_name="JWT Authentication"
)


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as exception:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=f"Невалидный токен {exception}"
        )
    return payload
