from fastapi import APIRouter, Depends

from app.api.schemas.projects_users_schems import ProjectUserRead, UserProjectsRead
from app.core.dependencies import get_project_management_service
from app.services.project_management_service import ProjectManagementService

router = APIRouter()


@router.get("/")
async def get_connections(
    project_management_service: ProjectManagementService = Depends(
        get_project_management_service
    ),
) -> list[ProjectUserRead]:
    """
    **Получает все связи проектов и пользователей**

    Returns:

        Список всех связей проектов и пользователей.
    """
    result: list[ProjectUserRead] = await project_management_service.get_connections()
    return result


@router.get("/{user_id}")
async def get_projects_by_user(
    user_id: int,
    project_management_service: ProjectManagementService = Depends(
        get_project_management_service
    ),
) -> UserProjectsRead:
    """
    **Получает все проекты одного пользователя**

    Args:

        user_id: id пользователя которого нужно добавить на проект.

        project_management_service: Сервис управляющий проектами.

    Returns:

        Проекты пользователя.
    """
    result: UserProjectsRead = await project_management_service.get_projects_by_user_id(
        user_id
    )
    return result


@router.get("/{project_id}/{user_id}")
async def get_connection(
    project_id: int,
    user_id: int,
    project_management_service: ProjectManagementService = Depends(
        get_project_management_service
    ),
) -> ProjectUserRead:
    """
    **Получает связь проекта и пользователя**

    Args:

        project_id: id проекта на который нужно добавить пользователя.

        user_id: id пользователя которого нужно добавить на проект.

        project_management_service: Сервис управляющий проектами.

    Returns:

        Связь проекта и пользователя.
    """
    result: ProjectUserRead = await project_management_service.get_connection(
        project_id, user_id
    )
    return result


@router.post("/{project_id}/{user_id}")
async def create_connectio(
    project_id: int,
    user_id: int,
    project_management_service: ProjectManagementService = Depends(
        get_project_management_service
    ),
) -> ProjectUserRead:
    """
    **Добавляет на проект пользователя**

    Args:
        project_id: id проекта на который нужно добавить пользователя.

        user_id: id пользователя которого нужно добавить на проект.

        project_management_service: Сервис управляющий проектами.


    Returns:

        Модель связи проекта и пользователя.
    """
    result: ProjectUserRead = await project_management_service.create_connection(
        project_id, user_id
    )
    return result


@router.delete("/{project_id}/{user_id}")
async def delete_connection(
    project_id: int,
    user_id: int,
    project_management_service: ProjectManagementService = Depends(
        get_project_management_service
    ),
) -> None:
    """
    **Удаление связи проекта и пользователя.**

    Удаляет данные о связи проекта и пользователя по его id.

    Args:
        project_id: id проекта на который нужно добавить пользователя.

        user_id: id пользователя которого нужно добавить на проект.

        project_management_service: Сервис управляющий проектами.
    """
    await project_management_service.delete_connection(project_id, user_id)
