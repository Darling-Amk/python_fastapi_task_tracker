from fastapi import Form
from fastapi.params import Depends

from app.api.exceptions import InvalidAuthError
from app.auth.repositories.user_auth_repository import UserAuthRepository
from app.auth.schemas.user_auth_schema import UserAuth
from app.auth.services.jwt_service import AuthJWTService
from app.auth.services.user_auth_service import UserAuthService


def get_jwt_service() -> AuthJWTService:
    return AuthJWTService()


def get_auth_user_service() -> UserAuthService:
    return UserAuthService(UserAuthRepository())


async def valid_auth_user(
    email: str = Form(),
    password: str = Form(),
    user_service: UserAuthService = Depends(get_auth_user_service),
) -> UserAuth:
    user: UserAuth = await user_service.get_user_by_email(email)

    if not await user_service.is_valid_auth_user(
        user=user, email=email, password=password
    ):
        raise InvalidAuthError()
    return user
