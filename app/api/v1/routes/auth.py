from app.api.v1.dependencies import UserValidateDep
from app.schemas.token import TokenSchema
from app.schemas.user import CreateUserSchema, UserSchema
from app.models.user import User
from fastapi import APIRouter
from app.core.security import hash_password
from app.utils.jwt import encode_jwt
from app.api.v1.dependencies import GetCurrentUserDep, AuthRepositoryDep
from app.api.v1.exceptions import AlreadyExistsException

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/", response_model=UserSchema)
async def register_user(
    schema: CreateUserSchema, repo: AuthRepositoryDep
) -> UserSchema:
    user = await repo.get_user_by_name(schema.username)
    if user:
        raise AlreadyExistsException(User.__name__)
    else:
        hashed_password = hash_password(schema.password)
        new_user = await repo.create_user(
            username=schema.username, password=hashed_password
        )
        return new_user


@router.post("/login/", response_model=TokenSchema)
async def auth_user(user: UserValidateDep):
    jwt_payload = {"sub": str(user.id), "username": user.username}
    token = encode_jwt(jwt_payload)
    return TokenSchema(access_token=token, token_type="Bearer")


@router.get("/users/me", response_model=UserSchema)
async def get_users_me(user: GetCurrentUserDep) -> UserSchema:
    return UserSchema.model_validate(user, from_attributes=True)
