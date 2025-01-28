from pydantic import EmailStr

from app.api.exceptions import UserAlreadyExistsError, InvalidAuthError
from app.api.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.auth.repositories.user_auth_repository import UserAuthRepository
from app.auth.schemas.user_auth_schema import UserAuth
from app.repositories.user_repository import UserRepository

from app.auth.services.password_service import PasswordService


class UserAuthService:

    def __init__(self, user_repository: UserAuthRepository):
        self.repository: UserAuthRepository = user_repository
        self.password_service: PasswordService = PasswordService()

    async def get_user_by_email(self, email: str | EmailStr) -> UserAuth:
        """
        Метод получает пользователя по его почте.
        Args:
            email: почти пользователя
        Returns:
            UserRead: Найденная модель пользователя, либо None, если пользователь не найден.
        """
        user: UserAuth | None = await self.repository.get_auth_user_by_email(email)
        if user is None:
            raise InvalidAuthError()

        return user

    async def is_valid_auth_user(
        self, user: UserAuth, email: str, password: str
    ) -> bool:
        return user.email == email and self.password_service.validate_password(
            password=password, hashed_password=user.password_hash
        )
