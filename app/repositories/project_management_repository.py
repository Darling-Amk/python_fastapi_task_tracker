from sqlalchemy import delete, select

from app.api.models.user_projects import UserProjects
from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.projects_users_schems import ProjectUserCreate, ProjectUserRead
from app.api.schemas.user_schema import UserRead
from app.db import async_session
from app.repositories.base import SQLAlchemyRepository


class ProjectManagementRepository(SQLAlchemyRepository):
    model = UserProjects

    async def get_connections(self) -> list[tuple[int, int]]:
        """
        Получает все связи проектов и пользователей
        Returns:
            Список всех связей проектов и пользователей (project_id, user_id)
        """
        async with async_session() as session:
            stmt = select(self.model.project_id, self.model.user_id)
            res = await session.execute(stmt)
            return res.all()

    async def get_connection(
        self,
        project: ProjectRead,
        user: UserRead,
    ) -> ProjectUserRead | None:
        """
        Получает связь между проектом и пользователем.
        Returns:
            Список всех связей проектов и пользователей.
        """

        async with async_session() as session:
            stmt = (
                select(self.model)
                .where(self.model.user_id == user.id)
                .where(self.model.project_id == project.id)
            )
            res = await session.execute(stmt)
            data = res.scalar_one_or_none()
            if data is None:
                return None
            return ProjectUserRead(project=project, user=user)

    async def get_projects_ids_by_user_id(
        self,
        user_id: int,
    ) -> list[int]:
        """
        Получает все проекты одного пользователя
        Args:
            user_id: id пользователя которого нужно добавить на проект.
        Returns:
            Проекты пользователя.
        """

        async with async_session() as session:
            stmt = select(self.model.project_id).where(self.model.user_id == user_id)
            res = await session.execute(stmt)
            ids = [row[0] for row in res.all()]
            print(ids)
            return ids

    async def delete_connection(self, connection_model: ProjectUserRead) -> None:
        """
        Удаление связи проекта и пользователя.
        Удаляет данные о связи проекта и пользователя по его id.

        Args:
            connection_model: модель связи проекта и пользователя.
        """

        async with async_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.user_id == connection_model.user.id)
                .where(self.model.project_id == connection_model.project.id)
            )

            res = await session.execute(stmt)
            await session.commit()  # Сохраняем изменения

    async def add_user_on_project(
        self, project: ProjectRead, user: UserRead
    ) -> ProjectUserRead:
        """
        Добавляет на проект пользователя.
        Args:
            project: проект на который нужно добавить пользователя.
            user: пользователь которого нужно добавить на проект.
        Returns:
            Модель связи проекта и пользователя.
        """
        model = ProjectUserCreate(project_id=project.id, user_id=user.id)
        await self.add_one(model.model_dump())
        return ProjectUserRead(user=user, project=project)
