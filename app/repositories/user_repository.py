from pydantic import EmailStr
from sqlalchemy import select

from app.api.exceptions import UserNotFoundError
from app.api.models.user import User
from app.api.schemas.user_schema import UserRead, UserCreate, UserUpdate
from app.db import async_session
from app.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def create_user(self, new_user: UserCreate, password_hash: bytes) -> UserRead:
        """
        Метод создания нового пользователя.
        Args:
            new_user: Данные нового пользователя.
            password_hash: Хешированный пароль пользователя.
        Returns:
            UserRead: Созданная модель пользователя.
        """
        new_user: User = await self.add_one(
            {
                "name": new_user.name,
                "email": new_user.email,
                "password_hash": password_hash,
            }
        )
        return new_user.to_read_model()

    async def is_email_already_exist(self, email: str | EmailStr) -> bool:
        """
        Метод проверяет занята ли почти.
        Args:
            email: почти пользователя
        Returns:
            bool: True, если пользователь существует, иначе False.
        """
        return await self.get_user_by_email(email) is not None

    async def get_user_by_email(self, email: str | EmailStr) -> UserRead | None:
        """
        Метод получает пользователя по его почте.
        Args:
            email: почти пользователя
        Returns:
            UserRead: Найденная модель пользователя, либо None, если пользователь не найден.
        """
        async with async_session() as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            user: User | None = result.scalar_one_or_none()
            return user

    async def get_user_by_id(self, user_id: int) -> UserRead:
        """
        Получение пользователя по его id.

        Args:
            user_id: id пользователя, которого необходимо получить.
        Raises:
            UserNotFoundError: пользователь не найден
        Returns:
           Ответ с данными пользователя.
        """
        user: UserRead | None = await self.get_read_model_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

    async def update_user(
        self, user_data: UserRead, new_password_hash: bytes | None
    ) -> UserRead:
        """
        Обновление информации о пользователе.
        Обновляет данные пользователя по его id. Возвращает обновлённого пользователя.
        Args:
            new_password_hash: новый хэш пароля(если пароль изменился)
            user_data: Данные, которые необходимо обновить.
        Returns:
            Обновлённый пользователь.
        """
        user: User = await self.get_model_by_id(user_data.id)

        user.password_hash = new_password_hash or user.password_hash
        user.name = user_data.name or user.name
        user.email = user_data.email or user.email

        return await self.update_one(user)

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя.
        Args:
            user_id: id пользователя которого нужно удалить.
        """
        user: UserRead | None = await self.get_read_model_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        await self.delete_one(user_id)
