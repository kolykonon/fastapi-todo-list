from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.db import SessionDep
from schemas import UserSchema
from utils import decode_jwt


def get_current_token_payload(
    session: SessionDep, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer)
) -> dict:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    return payload
