from app.api.exceptions import UserAlreadyExistsError
from app.repositories import UserRepository
from app.api.schemas.user_schema import (
    UserCreate,
    UserCreateWithPasswordHash,
    UserRead,
    UserUpdate,
    UserUpdateWithPasswordHash,
)


class UserService:
    """
    Сервис отвечающий за работу с пользователями

    """

    def __init__(self, user_repository: UserRepository):
        self.repository: UserRepository = user_repository

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

        new_user: UserCreateWithPasswordHash = self.add_hash(user_data)
        new_user: UserRead = await self.repository.add_user(new_user)
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
        updated_user: UserUpdateWithPasswordHash = UserUpdateWithPasswordHash(
            id=user_id
        )

        if user_data.password:
            # TODO hash
            updated_user.password_hash = user_data.password

        if user_data.name:
            updated_user.name = user_data.name

        if user_data.email and user_data.email != user.email:
            if await self.repository.is_email_already_exist(user_data.email):
                raise UserAlreadyExistsError()
            updated_user.email = str(user_data.email)

        updated_user: UserRead = await self.repository.update_user(updated_user)
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

    def add_hash(self, user_data: UserCreate) -> UserCreateWithPasswordHash:
        new_user: UserCreateWithPasswordHash = UserCreateWithPasswordHash(
            name=user_data.name,
            email=user_data.email,
            password_hash=user_data.password,
        )
        return new_user
