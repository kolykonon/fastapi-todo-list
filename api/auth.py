from fastapi import APIRouter
from schemas import CreateUserSchema, UserSchema
from core import SessionDep
from models import User
from sqlalchemy import select
from fastapi import HTTPException, status
from core.utils import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/")
async def register_user(schema: CreateUserSchema, session: SessionDep):
    query = select(User).where(User.email == schema.email)
    user = await session.execute(query)
    if user.one_or_none():
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Пользователь с таким email уже существует!"
        )
    else:
        hashed_password = hash_password(schema.password)
        user = User(email=schema.email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    return {"Ok": True}
