from typing import Annotated
from fastapi import Depends
from app.core.exceptions import AlreadyExistsException
from app.core.security import hash_password
from app.models.user import User
from app.repositories.auth_repository import AuthRepositoryDep
from app.schemas.token import TokenSchema
from app.schemas.user import CreateUserSchema
from app.services.dependencies import GetCurrentUserDep
from app.utils.jwt import encode_jwt


class UserService:
    def __init__(self, repository: AuthRepositoryDep):
        self.repository = repository

    async def register_user(self, data: CreateUserSchema):
        user = await self.repository.get_user_by_name(data.username)
        if user:
            raise AlreadyExistsException(User)
        else:
            hashed_password = hash_password(data.password)
            new_user = await self.repository.create_user(
                username=data.username, password=hashed_password
            )
            return new_user

    async def auth_user(self, user: GetCurrentUserDep):
        jwt_payload = {"sub": str(user.id), "username": user.username}
        token = encode_jwt(jwt_payload)
        return TokenSchema(access_token=token, token_type="Bearer")

    async def get_user_info(self, user: GetCurrentUserDep):
        return user


def get_user_service(repository: AuthRepositoryDep):
    return UserService(repository=repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
