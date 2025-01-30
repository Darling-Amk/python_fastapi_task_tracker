from typing import Dict, Any

from fastapi import Form
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr

from app.api.exceptions import InvalidAuthError
from app.api.exceptions.auth_errors import InvalidJWTError
from app.auth import http_bearer
from app.auth.models.payload_dict import UserPayload
from app.auth.repositories.user_auth_repository import UserAuthRepository
from app.auth.schemas.user_auth_schema import UserAuth
from app.auth.services.jwt_service import AuthJWTService
from app.auth.services.payload_service import PayloadService
from app.auth.services.user_auth_service import UserAuthService


async def get_jwt_service() -> AuthJWTService:
    """
    Зависимость возвращает экземпляр сервиса JWT.

    Returns:
        AuthJWTService: Экземпляр сервиса JWT.
    """
    return AuthJWTService()


async def get_auth_user_service() -> UserAuthService:
    """
    Зависимость возвращает экземпляр сервиса аутентификации пользователей.

    Returns:
        UserAuthService: Экземпляр сервиса аутентификации пользователей.
    """
    return UserAuthService(UserAuthRepository())


async def get_current_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    jwt_service: AuthJWTService = Depends(get_jwt_service),
) -> UserPayload:
    """
    Зависимость возвращает текущий payload из токена.
    Декодирует JWT-токен и извлекает payload.

    Args:
        credentials: Учетные данные авторизации.
        jwt_service: Сервис для работы с JWT-токеном.
    Returns:
        UserPayload: Объект данных пользователя.
    Raises:
        InvalidJWTError: Если токен не может быть декодирован.
    """
    raw_token = credentials.credentials
    try:
        raw_payload: Dict[str, Any] = jwt_service.decode_jwt(raw_token)
    except Exception:
        raise InvalidJWTError()

    user_payload: UserPayload = PayloadService.payload2user_payload(raw_payload)
    return user_payload


async def get_current_user(
    user_service: UserAuthService = Depends(get_auth_user_service),
    payload: UserPayload = Depends(get_current_payload),
) -> UserAuth:
    """
    Получает текущего пользователя по payload.
    Получает информацию о пользователе из базы данных на основе payload.

    Args:
        user_service: Сервис для работы с пользователями.
        payload: Данные пользователя.

    Returns:
        UserAuth: Объект аутентифицированного пользователя.
    """
    user: UserAuth = await user_service.get_user_by_user_payload(payload)
    return user


async def valid_auth_user(
    email: EmailStr = Form(),
    password: str = Form(),
    user_service: UserAuthService = Depends(get_auth_user_service),
) -> UserAuth:
    """
    Проверяет подлинность пользователя по электронной почте и паролю.

    Получает пользователя по электронной почте и проверяет пароль.

    Args:
        email: Электронная почта пользователя.
        password: Пароль пользователя.
        user_service: Сервис для работы с пользователями.

    Returns:
        UserAuth: Объект аутентифицированного пользователя.

    Raises:
        InvalidAuthError: Если пользователь не найден или пароль неверный.
    """
    user: UserAuth = await user_service.get_user_by_email(email)

    if not await user_service.is_valid_auth_user(
        user=user, email=email, password=password
    ):
        raise InvalidAuthError()
    return user
