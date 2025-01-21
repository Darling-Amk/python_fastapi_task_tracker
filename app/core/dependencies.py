from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository, ProjectRepository
from app.repositories.project_management_repository import ProjectManagementRepository
from app.services import UserService, ProjectService
from app.db import async_session
from app.services.project_management_service import ProjectManagementService


# Асинхронный генератор сессий (Depends)
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_user_service() -> UserService:
    return UserService(UserRepository())


def get_project_service() -> ProjectService:
    return ProjectService(ProjectRepository())


def get_project_management_service() -> ProjectManagementService:
    user_service: UserService = get_user_service()
    project_service: ProjectService = get_project_service()
    return ProjectManagementService(
        ProjectManagementRepository(), user_service, project_service
    )


# async def get_task_service() -> ProjectService:
#     return TaskService(TaskRepository)
