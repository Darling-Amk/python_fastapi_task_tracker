from app.api.exceptions import ProjectNotFoundError, UserNotFoundError
from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.user_schema import (
    UserRead,
)
from app.repositories import UserRepository, ProjectRepository
from app.repositories.project_user_repository import ProjectUserRepository
from app.services import ProjectService, UserService


class ProjectUserService:
    """
    Сервис отвечающий за работу с пользователями

    """

    def __init__(self, project_user_repository: ProjectUserRepository):
        self.repository: ProjectUserRepository = project_user_repository
        self.project_service: ProjectService = ProjectService(ProjectRepository())
        self.user_service: UserService = UserService(UserRepository())

    async def add_user(self, project_id: int, user_id: int):
        """
        Получить список всех проектов.
        Args:
            project_id: id проекта на который нужно добавить пользователя.
            user_id: id пользователя которого нужно добавить на проект.
        """
        project: ProjectRead = await self.project_service.get_project(project_id)

        if project is None:
            raise ProjectNotFoundError()

        user: UserRead | None = await self.user_service.get_user(user_id)
        if user is None:
            raise UserNotFoundError()

        await self.repository.add_user(project_id, user_id)
