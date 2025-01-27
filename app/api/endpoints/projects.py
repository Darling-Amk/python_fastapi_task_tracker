from fastapi import APIRouter, Depends

from app.api.schemas.project_schema import (ProjectCreate, ProjectRead,
                                            ProjectUpdate)
from app.core.dependencies import get_project_service
from app.services import ProjectService

router = APIRouter()


@router.get("/")
async def get_projects(
    project_service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    """
    **Получение список всех проектов.**

    Returns:

        Список проектов.
    """
    projects: list[ProjectRead] = await project_service.get_projects()
    return projects


@router.post("/")
async def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """
    **Создание нового проекта.**

    Args:

        project_data: Данные для создания проекта.

        project_service: Сервис управляющий проектами.


    Returns:

        Ответ с id созданного проекта.
    """

    new_project: ProjectRead = await project_service.create_project(project_data)
    return new_project


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """
    **Получить проект по его id.**

    Args:

        project_id: id проекта, который необходимо получить.

        project_service: Сервис управляющий проектами.

    Returns:

       Ответ с данными проекта или None, если проект не найден.
    """

    project: ProjectRead = await project_service.get_project(project_id)
    return project


@router.put("/{project_id}")
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    """
    **Обновление информации о проекте.**

    Обновляет данные проекта по его id. Возвращает обновлённый проект.

    Args:
        project_id: id проекта, которого нужно обновить.

        project_data: Данные, которые необходимо обновить.

        project_service: Сервис управляющий проектами.


    Returns:

        Обновлённый проект.
    """
    updated_project: ProjectRead = await project_service.update_project(
        project_id, project_data
    )
    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service),
) -> None:
    """
    **Удаление проекта.**

    Удаляет данные о проекте по его id.

    Args:
        project_id: id проекта которого нужно удалить.

        project_service: Сервис управляющий проектами.


    Returns:

        Обновлённый проект.
    """
    result = await project_service.delete_project(project_id)
