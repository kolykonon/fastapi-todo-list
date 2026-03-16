from api.v1.dependencies import UserValidateDep
from schemas.token import TokenSchema
from schemas.user import CreateUserSchema
from core.db import SessionDep
from models.user import User
from sqlalchemy import select
from fastapi import Depends, HTTPException, status, APIRouter
from core.security import hash_password
from utils.jwt import encode_jwt
from api.v1.dependencies import GetCurrentUserDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(schema: CreateUserSchema, session: SessionDep):
    query = select(User).where(User.username == schema.username)
    user = await session.execute(query)
    if user.scalar_one_or_none():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Пользователь с таким email уже существует!"
        )
    else:
        hashed_password = hash_password(schema.password)
        user = User(username=schema.username, password=hashed_password)
    session.add(user)
    await session.commit()
    return {"Ok": True}


@router.post("/login/", response_model=TokenSchema)
async def auth_user(user: UserValidateDep):
    jwt_payload = {"sub": str(user.id), "username": user.username}
    token = encode_jwt(jwt_payload)
    return TokenSchema(access_token=token, token_type="Bearer")


@router.get("/users/me")
async def get_users_me(user: GetCurrentUserDep) -> dict:
    return {"email": user.username}
