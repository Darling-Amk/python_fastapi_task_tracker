from app.api.exceptions import (
    ProjectConnectionNotFoundError,
    ProjectConnectionAlreadyExist,
)
from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.projects_users_schems import ProjectUserRead, UserProjectsRead
from app.api.schemas.user_schema import UserRead
from app.repositories.project_management_repository import ProjectManagementRepository
from app.services import ProjectService, UserService


class ProjectManagementService:
    """
    Сервис отвечающий за управление проектами.
    Назначение и удаление с них людей.

    """

    def __init__(
        self,
        project_repository: ProjectManagementRepository,
        user_service,
        project_service,
    ):
        self.repository: ProjectManagementRepository = project_repository
        self.user_service: UserService = user_service
        self.project_service: ProjectService = project_service

    async def get_connection(self, project_id: int, user_id: int) -> ProjectUserRead:
        """
        Получает связь между проектом и пользователем.
        Args:
            project_id: id проекта на который нужно добавить пользователя.
            user_id: id пользователя которого нужно добавить на проект.
        Returns:
            Связь проекта и пользователя.
        """
        user: UserRead = await self.user_service.get_user(user_id)
        project: ProjectRead = await self.project_service.get_project(project_id)

        model: ProjectUserRead | None = await self.repository.get_connection(
            project=project, user=user
        )
        if model is None:
            raise ProjectConnectionNotFoundError()
        return model

    async def get_projects_by_user_id(
        self,
        user_id: int,
    ) -> UserProjectsRead:
        """
        Получает все проекты одного пользователя
        Args:
            user_id: id пользователя которого нужно добавить на проект.
        Returns:
            Проекты пользователя.
        """
        user: UserRead = await self.user_service.get_user(user_id)

        project_ids: list[int] = await self.repository.get_projects_ids_by_user_id(
            user_id
        )

        projects: list[ProjectRead] = await self.project_service.get_projects_by_ids(
            project_ids
        )

        return UserProjectsRead(user=user, projects=projects)

    async def get_connections(self) -> list[ProjectUserRead]:
        """
        Получает все связи проектов и пользователей
        Returns:
            Список всех моделей связей проектов и пользователей.
        """
        return [
            ProjectUserRead(
                user=await self.user_service.get_user(user_id),
                project=await self.project_service.get_project(project_id),
            )
            for project_id, user_id in await self.repository.get_connections()
        ]

    async def create_connection(self, project_id: int, user_id: int) -> ProjectUserRead:
        """
        Добавляет на проект пользователя.
        Args:
            project_id: id проекта на который нужно добавить пользователя.
            user_id: id пользователя которого нужно добавить на проект.
        Returns:
            Модель связи проекта и пользователя.
        """
        user: UserRead = await self.user_service.get_user(user_id)
        project: ProjectRead = await self.project_service.get_project(project_id)

        if await self.repository.get_connection(project=project, user=user) is not None:
            raise ProjectConnectionAlreadyExist()

        project_user: ProjectUserRead = await self.repository.add_user_on_project(
            project, user
        )
        return project_user

    async def delete_connection(self, project_id: int, user_id: int) -> None:
        """
        Удаление связи проекта и пользователя.
        Удаляет данные о связи проекта и пользователя по его id.

        Args:
            project_id: id проекта на который нужно добавить пользователя.

            user_id: id пользователя которого нужно добавить на проект.

        """

        user: UserRead = await self.user_service.get_user(user_id)
        project: ProjectRead = await self.project_service.get_project(project_id)

        connection_model: ProjectUserRead | None = await self.repository.get_connection(
            project=project, user=user
        )
        if connection_model is None:
            raise ProjectConnectionNotFoundError(
                "Удаляемая связь между пользователем и проектом уже не существует"
            )
        await self.repository.delete_connection(connection_model)
