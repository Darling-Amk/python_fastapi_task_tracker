from app.api.models.task import Task
from app.api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.repositories.base import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task

    async def add_task(self, new_task: TaskCreate) -> TaskRead:
        """
        Добавляет новую задачу в базу данных.
        Args:
            new_task: Данные для создания задачи.
        Returns:
            TaskRead: Ответ с информацией о созданной задаче.
        """
        new_task: Task = await self.add_one(new_task.model_dump())

        return new_task.to_read_model()

    async def get_task_by_id(self, task_id: int) -> TaskRead | None:
        """
        Получение задачи по её id.
        Args:
            task_id: id задачи, которую необходимо получить.
        Raises:
            TaskNotFoundError: задача не найдена.
        Returns:
           Ответ с данными пользователя.
        """
        task: TaskRead | None = await self.get_read_model_by_id(task_id)
        return task

    async def update_task(self, task_id: int, updated_task: TaskUpdate) -> TaskRead:
        """
        Обновление информации о задаче.
        Обновляет данные задачи по её id. Возвращает обновлённую задачу.
        Args:
            task_id: id задачи, которую необходимо обновить.
            updated_task: Данные, которые необходимо обновить.
        Returns:
            Обновленная задача
        """
        task: Task = await self.get_model_by_id(task_id)

        task.title = updated_task.title or task.title
        task.description = updated_task.description or task.description
        task.status = updated_task.status or task.status
        task.due_date = updated_task.due_date or task.due_date
        task.project_id = updated_task.project_id or task.project_id
        task.assigned_user_id = updated_task.assigned_user_id or task.assigned_user_id

        task: TaskRead = await self.update_one(task)

        return task

    async def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу по id.
        Args:
            task_id: id задачи которую нужно удалить.
        """

        await self.delete_one(task_id)
