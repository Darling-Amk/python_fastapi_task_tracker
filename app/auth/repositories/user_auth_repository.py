from pydantic import EmailStr
from sqlalchemy import select

from app.api.models import User
from app.auth.schemas.user_auth_schema import UserAuth
from app.db import async_session
from app.repositories import UserRepository


class UserAuthRepository(UserRepository):
    model = User

    async def get_auth_user_by_email(self, email: str | EmailStr) -> UserAuth | None:
        """
        Метод получает пользователя по его почте.
        Args:
            email: почти пользователя
        Returns:
            UserAuth: Найденная модель пользователя, либо None, если пользователь не найден.
        """
        async with async_session() as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user: User | None = result.scalar_one_or_none()
            if user is None:
                return None
            return UserAuth(
                email=user.email,
                password_hash=user.password_hash,
                id=user.id,
                name=user.name,
            )
