from app.schemas.token import TokenSchema
from app.schemas.user import CreateUserSchema, UserSchema
from fastapi import APIRouter
from app.services.dependencies import GetCurrentUserDep, ValidateUserDep
from app.services.user_service import UserServiceDep

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/", response_model=UserSchema)
async def register_user(
    schema: CreateUserSchema, service: UserServiceDep
) -> UserSchema:
    return await service.register_user(data=schema)


@router.post("/login/", response_model=TokenSchema)
async def auth_user(service: UserServiceDep, user: ValidateUserDep):
    return await service.auth_user(user=user)


@router.get("/users/me", response_model=UserSchema)
async def get_users_me(service: UserServiceDep, user: GetCurrentUserDep) -> UserSchema:
    return await service.get_user_info(user=user)
