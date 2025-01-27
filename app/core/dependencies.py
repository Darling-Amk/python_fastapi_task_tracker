from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.repositories import ProjectRepository, UserRepository
from app.repositories.project_management_repository import \
    ProjectManagementRepository
from app.repositories.task_repository import TaskRepository
from app.services import ProjectService, UserService
from app.services.project_management_service import ProjectManagementService
from app.services.task_service import TaskService


# Асинхронный генератор сессий (Depends)
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


def get_user_service() -> UserService:
    return UserService(UserRepository())


def get_project_service() -> ProjectService:
    return ProjectService(ProjectRepository())

def get_task_service() -> TaskService:
    user_service: UserService = get_user_service()
    project_service: ProjectService = get_project_service()
    return TaskService(TaskRepository(),user_service,project_service)


def get_project_management_service() -> ProjectManagementService:
    user_service: UserService = get_user_service()
    project_service: ProjectService = get_project_service()
    return ProjectManagementService(
        ProjectManagementRepository(), user_service, project_service
    )


# async def get_task_service() -> ProjectService:
#     return TaskService(TaskRepository)
