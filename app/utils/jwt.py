import jwt as pyjwt
from core.config import settings
from datetime import datetime, timedelta
import bcrypt

auth_jwt = settings.jwt_settings


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    expire = datetime.now() + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=datetime.now())

    encoded = pyjwt.encode(
        payload, private_key, algorithm=settings.jwt_settings.algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = pyjwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
