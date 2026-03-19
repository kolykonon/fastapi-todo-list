from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy import select
from app.models.user import User
from app.core.db import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession


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


def get_auth_repositoty(session: SessionDep):
    return AuthRepository(session)


AuthRepositoryDep = Annotated[AuthRepository, Depends(get_auth_repositoty)]
