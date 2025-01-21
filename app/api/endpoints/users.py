from fastapi import APIRouter, Depends

from app.api.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.core.dependencies import get_user_service
from app.services import UserService

router = APIRouter()


@router.get("/")
async def get_users(
    user_service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    """
    **Получение список всех пользователей.**

    Returns:

        Список пользователей.
    """
    users: list[UserRead] = await user_service.get_users()
    return users


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    **Получение пользователя по его id.**

    Args:

        user_id: id пользователя, которого необходимо получить.

        user_service: Сервис управляющий пользователями.

    Returns:

       Ответ с данными пользователя или None, если пользователь не найден.
    """

    user: UserRead = await user_service.get_user(user_id)
    return user


@router.post("/")
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    **Создание нового пользователя.**

    Проверяет, существует ли пользователь с таким email, если нет, то создает нового пользователя.

    Args:

        user_data: Данные для создания пользователя.

        user_service: Сервис управляющий пользователями.


    Returns:

        Ответ с id созданного пользователя.
    """

    new_user: UserRead = await user_service.create_user(user_data)
    return new_user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """
    **Обновление информации о пользователе.**

    Обновляет данные пользователя по его id. Возвращает обновлённого пользователя.

    Args:
        user_id: id пользователя, которого нужно обновить.

        user_data: Данные, которые необходимо обновить.

        user_service: Сервис управляющий пользователями.


    Returns:

        Обновлённый пользователь.
    """
    updated_user: UserRead = await user_service.update_user(user_id, user_data)
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> None:
    """
    **Удаление пользователя.**

    Удаляет данные о пользователе по его id.

    Args:
        user_id: id пользователя которого нужно удалить.

        user_service: Сервис управляющий пользователями.


    Returns:

        Обновлённый пользователь.
    """
    result = await user_service.delete_user(user_id)
