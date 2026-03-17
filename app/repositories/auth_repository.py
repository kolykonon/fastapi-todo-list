from typing import Optional
from sqlalchemy import select
from models.user import User
from core.db import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import CreateUserSchema


class AuthRepository:
    def __init__(self, session: SessionDep):
        self.session: AsyncSession = session

    async def get_user_by_name(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def create_user(self, username: str, password: str) -> User:
        new_user = User(username=username, password=password)
        self.session.add(new_user)
        await self.session.commit()
        return new_user
