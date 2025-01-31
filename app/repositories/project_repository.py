from app.api.exceptions.project_errors import ProjectNotFoundError
from app.api.models.project import Project
from app.api.schemas.project_schema import ProjectCreate, ProjectRead
from app.repositories.base import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository):
    model = Project

    async def add_project(self, new_project: ProjectCreate) -> ProjectRead:
        new_project: Project = await self.add_one(new_project.model_dump())
        return new_project.to_read_model()

    async def get_project_by_id(self, project_id: int) -> ProjectRead | None:
        """
        Получение проекта по его id.
        Args:
            project_id: id проекта, которого необходимо получить.
        Raises:
            ProjectNotFoundError: проект не найден.
        Returns:
           Ответ с данными пользователя.
        """
        project: ProjectRead | None = await self.get_read_model_by_id(project_id)
        return project

    async def update_project(self, updated_project: ProjectRead) -> ProjectRead:
        """
        Обновление информации о пользователе.
        Обновляет данные пользователя по его id. Возвращает обновлённого пользователя.
        Args:
            updated_project: Данные, которые необходимо обновить.
        Returns:
            Обновлённый пользователь.
        """
        project: Project = await self.get_model_by_id(updated_project.id)

        if project is None:
            raise ProjectNotFoundError()

        if project.name:
            project.name = updated_project.name
        if project.description:
            project.description = updated_project.description

        project: ProjectRead = await self.update_one(project)

        return project

    async def delete_project(self, project_id: int) -> None:
        """
        Удаляет пользователя.
        Args:
            project_id: id пользователя которого нужно удалить.
        """
        project: ProjectRead | None = await self.get_read_model_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError()

        await self.delete_one(project_id)

    async def add_user(self, new_project: ProjectCreate) -> ProjectRead:
        new_project: Project = await self.add_one(new_project.model_dump())
        return new_project.to_read_model()
