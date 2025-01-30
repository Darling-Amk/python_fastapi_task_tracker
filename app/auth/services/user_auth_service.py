from pydantic import EmailStr

from app.api.exceptions import InvalidAuthError
from app.api.schemas.user_schema import UserRead
from app.auth.models.payload_dict import UserPayload
from app.auth.repositories.user_auth_repository import UserAuthRepository
from app.auth.schemas.user_auth_schema import UserAuth
from app.auth.services.password_service import PasswordService


class UserAuthService:

    def __init__(self, user_repository: UserAuthRepository):
        self.repository: UserAuthRepository = user_repository
        self.__password_service: PasswordService = PasswordService()

    async def get_user_by_user_payload(self, user_payload: UserPayload) -> UserAuth:
        """
        Метод получает пользователя по user_payload
        Args:
            user_payload: payload словарь с полями sub, name, email
        Returns:
            UserRead: Найденная модель пользователя
        """
        user: UserAuth = await self.get_user_by_email(user_payload.get("email"))
        return user

    async def get_user_by_email(self, email: str | EmailStr) -> UserAuth:
        """
        Метод получает пользователя по его почте.
        Args:
            email: почта пользователя
        Raises:
            InvalidAuthError: нет пользователя с такой почтой.
        Returns:
            UserRead: Найденная модель пользователя, либо None, если пользователь не найден.
        """
        user: UserAuth | None = await self.repository.get_auth_user_by_email(email)
        if user is None:
            raise InvalidAuthError()

        return user

    async def is_valid_auth_user(
        self, user: UserAuth, email: str | EmailStr, password: str
    ) -> bool:
        return user.email == email and self.__password_service.validate_password(
            password=password, hashed_password=user.password_hash
        )
