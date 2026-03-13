import jwt
from core import settings

auth_jwt = settings.jwt_settings


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload, private_key, algorithm=settings.jwt_settings.algorithm
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
