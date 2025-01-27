from pydantic import EmailStr
from sqlalchemy import select

from app.api.exceptions import UserNotFoundError
from app.api.models import User
from app.api.schemas.user_schema import (UserCreateWithPasswordHash, UserRead,
                                         UserUpdateWithPasswordHash)
from app.db import async_session
from app.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def add_user(self, new_user: UserCreateWithPasswordHash) -> UserRead:
        new_user: User = await self.add_one(new_user.model_dump())
        return new_user.to_read_model()

    async def is_email_already_exist(self, email: str | EmailStr) -> bool:
        """
        Метод проверяет занята ли почти.
        Args:
            email: почти пользователя
        Returns:
           True или False
        """
        return await self.get_user_by_email(email) is not None

    async def get_user_by_email(self, email: str | EmailStr) -> UserRead | None:
        """
        Метод получает пользователя по его почте или возвращает None если его нет.
        Args:
            email: почти пользователя
        Returns:
           Модель пользователя.
        """
        async with async_session() as session:
            stmt = select(self.model).where(self.model.email == email)
            res = await session.execute(stmt)
            user: User | None = res.scalar_one_or_none()
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

    async def update_user(self, user_data: UserUpdateWithPasswordHash) -> UserRead:
        """
        Обновление информации о пользователе.
        Обновляет данные пользователя по его id. Возвращает обновлённого пользователя.
        Args:
            user_data: Данные, которые необходимо обновить.
        Returns:
            Обновлённый пользователь.
        """
        user: User = await self.get_model_by_id(user_data.id)
        if user_data.password_hash:
            user.password_hash = user_data.password_hash
        if user_data.name:
            user.name = user_data.name
        if user_data.email:
            user.email = user_data.email

        user: UserRead = await self.update_one(user)
        return user

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
