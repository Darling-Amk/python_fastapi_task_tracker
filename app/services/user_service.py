from app.api.exceptions import UserAlreadyExistsError
from app.api.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import UserRepository

from app.services.password_service import PasswordService


class UserService:
    """
    Сервис отвечающий за работу с пользователями

    """

    def __init__(self, user_repository: UserRepository):
        self.repository: UserRepository = user_repository
        self.password_service: PasswordService = PasswordService()

    async def get_users(self) -> list[UserRead]:
        """
        Получить список всех пользователей.
        Returns:
            Список пользователей.
        """
        users: list[UserRead] = await self.repository.find_all()
        return users

    async def get_user(self, user_id: int) -> UserRead:
        """
        Получить пользователя по его id.
        Выполняет асинхронный запрос для извлечения пользователя по заданному id.
        Если пользователь не найден, вызывает ошибку.
        Args:
            user_id: id пользователя, которого необходимо получить.
        Returns:
           Ответ с данными пользователя.
        """
        user: UserRead = await self.repository.get_user_by_id(user_id)
        return user

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """
        Создание нового пользователя.
        Проверяет, существует ли пользователь с таким email, если нет, то создает нового пользователя.
        Args:
            user_data: Данные для создания пользователя.
        Raises:
            UserAlreadyExistsError: пользователь с такой почтой уже зарегистрирован.
        Returns:
            UserRead: Ответ с информацией о созданном пользователе.
        """
        if await self.repository.is_email_already_exist(user_data.email):
            raise UserAlreadyExistsError()
        password_hash: bytes = self.password_service.hash_password(user_data.password)
        new_user: UserRead = await self.repository.create_user(
            new_user=user_data, password_hash=password_hash
        )
        return new_user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserRead:
        """
        Обновление информации о пользователе.
        Обновляет данные пользователя по его id. Возвращает обновлённого пользователя.
        Args:
            user_id: id пользователя, которого нужно обновить.
            user_data: Данные, которые необходимо обновить.
        Returns:
            Обновлённый пользователь.
        """
        user: UserRead = await self.repository.get_user_by_id(user_id)

        new_password_hash: None | bytes = None
        if user_data.password is not None:
            new_password_hash = self.password_service.hash_password(user_data.password)

        if user_data.email and user_data.email != user.email:
            if await self.repository.is_email_already_exist(user_data.email):
                raise UserAlreadyExistsError()
            user.email = user_data.email

        user.name = user_data.name or user.name
        updated_user: UserRead = await self.repository.update_user(
            user, new_password_hash
        )
        return updated_user

    async def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя.
        Args:
            user_id: id пользователя которого нужно удалить.
        Returns:
            Обновлённый пользователь.
        """
        await self.repository.delete_user(user_id)
