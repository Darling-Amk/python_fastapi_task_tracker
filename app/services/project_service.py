from app.api.exceptions import ProjectNotFoundError
from app.api.schemas.project_schema import ProjectCreate, ProjectRead, ProjectUpdate
from app.repositories import ProjectRepository


class ProjectService:
    """
    Сервис отвечающий за работу с проектами

    """

    def __init__(self, project_repository: ProjectRepository):
        self.repository: ProjectRepository = project_repository

    async def get_projects(self) -> list[ProjectRead]:
        """
        Получить список всех проектов.
        Returns:
            Список проектов.
        """
        projects: list[ProjectRead] = await self.repository.find_all()
        return projects

    async def get_project(self, project_id: int) -> ProjectRead:
        """
        Получение проекта по его id.

        Args:
            project_id: id проект, которого необходимо получить.
        Returns:
           Ответ с данными проект.
        """
        project: None | ProjectRead = await self.repository.get_project_by_id(
            project_id
        )

        if project is None:
            raise ProjectNotFoundError()

        return project

    async def create_project(self, project_data: ProjectCreate) -> ProjectRead:
        """
        Создание нового проекта.
        Args:
            project_data: Данные для создания проекта.
        Returns:
            ProjectRead: Ответ с информацией о созданном пользователе.
        """

        new_project: ProjectRead = await self.repository.add_project(project_data)
        return new_project

    async def update_project(
        self, project_id: int, project_data: ProjectUpdate
    ) -> ProjectRead:
        """
        Обновление информации о пользователе.
        Обновляет данные проект по его id. Возвращает обновлённого проект.
        Args:
            project_id: id проекта, который нужно обновить.
            project_data: Данные, которые необходимо обновить.
        Returns:
            Обновлённый проект.
        """
        project: ProjectRead = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ProjectNotFoundError()

        if project.name is not None:
            project.name = project_data.name

        if project.description is not None:
            project.description = project_data.description

        project: ProjectRead = await self.repository.update_project(project)
        return project

    async def delete_project(self, project_id: int) -> None:
        """
        Удаляет проект.
        Args:
            project_id: id проекта который нужно удалить.
        Returns:
            Обновлённый проект.
        """
        await self.repository.delete_project(project_id)

    async def get_projects_by_ids(self, project_ids: list[int]) -> list[ProjectRead]:
        """
        Получение списка проектов по списку id.

        Args:
            project_ids: списка id проектов.
        Returns:
           Список проектов
        """

        projects: list[ProjectRead] = [
            await self.get_project(project_id) for project_id in project_ids
        ]
        return projects
