from app.api.exceptions.task_errors import TaskNotFoundError
from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.api.schemas.user_schema import UserRead
from app.repositories.task_repository import TaskRepository
from app.services import ProjectService, UserService


class TaskService:
    """
    Сервис отвечающий за работу с задачами

    """

    def __init__(self, task_repository: TaskRepository, user_service, project_service):
        self.repository: TaskRepository = task_repository

        self.user_service: UserService = user_service
        self.project_service: ProjectService = project_service

    async def get_tasks(self) -> list[TaskRead]:
        """
        Получить список всех задач.
        Returns:
            Список задач.
        """
        tasks: list[TaskRead] = await self.repository.find_all()
        return tasks

    async def get_task(self, task_id: int) -> TaskRead:
        """
        Получение задачу по её id.

        Args:
            task_id: id задача, которую необходимо получить.
        Returns:
           Ответ с данными задачи.
        """
        task: None | TaskRead = await self.repository.get_task_by_id(task_id)

        if task is None:
            raise TaskNotFoundError()

        return task

    async def create_task(self, task_data: TaskCreate) -> TaskRead:
        """
        Создание новой задачи.
        Args:
            task_data: Данные для создания задачи.
        Returns:
            TaskRead: Ответ с информацией о созданной задаче.
        """
        user: UserRead = await self.user_service.get_user(task_data.assigned_user_id)
        project: ProjectRead = await self.project_service.get_project(
            task_data.project_id
        )

        new_task: TaskRead = await self.repository.add_task(task_data)
        return new_task

    async def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskRead:
        """
        Обновление информации о задаче.
        Обновляет данные задачи по её id. Возвращает обновлённую задачу.
        Args:
            task_id: id задачи, который нужно обновить.
            task_data: Данные, которые необходимо обновить.
        Raises:
            TaskNotFoundError: Если задача с указанным ID не найдена.
        Returns:
            Обновлённый задача.
        """
        task: TaskRead = await self.repository.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()

        updated_task: TaskRead = await self.repository.update_task(task.id, task_data)
        return updated_task

    async def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу.
        Raises:
            TaskNotFoundError: Если задача с указанным ID не найдена.
        Args:
            task_id: id задачи которую нужно удалить.
        """

        task: TaskRead = await self.repository.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        await self.repository.delete_task(task.id)
