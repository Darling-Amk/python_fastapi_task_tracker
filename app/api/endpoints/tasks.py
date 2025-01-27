from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from app.api.models.task_status import TaskStatus
from app.api.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.core.dependencies import get_task_service
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/")
async def get_tasks(
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskRead]:
    """
    **Получение списка всех задач.**

    Returns:

        Список задач.
    """
    tasks: list[TaskRead] = await task_service.get_tasks()
    return tasks


@router.post("/")
async def create_task(
    title: str,
    description: str,
    status: TaskStatus,
    project_id: int,
    assigned_user_id: int,
    due_date: datetime = datetime.now() + timedelta(days=7),
    created_at: datetime = datetime.now(),
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """
    **Создание новой задачи.**

    Args:

        title: Заголовок задачи.

        description: Описание задачи.

        status: Статус задачи.

        project_id: Идентификатор проекта, к которому относится задача.

        assigned_user_id: Идентификатор пользователя, ответственного за выполнение задачи.

        due_date: Срок выполнения задачи. По умолчанию через 7 дней от текущего момента.

        created_at: Дата создания задачи. По умолчанию текущее время.


    Returns:

         TaskRead: Ответ с информацией о созданной задаче.
    """

    new_task: TaskRead = await task_service.create_task(
        TaskCreate(
            title=title,
            description=description,
            status=status,
            project_id=project_id,
            assigned_user_id=assigned_user_id,
            created_at=created_at,
            due_date=due_date,
        )
    )
    return new_task


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """
    **Получение задачи по её id.**

    Args:

        task_id: id задачи, который необходимо получить.

        task_service: Сервис управляющий задачами.

    Returns:

       Ответ с данными задачи или None, если проект не найден.
    """

    task: TaskRead = await task_service.get_task(task_id)
    return task


@router.put("/{task_id}")
async def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    status: None | TaskStatus = None,
    project_id: int | None = None,
    assigned_user_id: int | None = None,
    due_date: datetime | None = None,
    task_service: TaskService = Depends(get_task_service),
) -> TaskRead:
    """
    **Обновление информации о проекте.**

    Обновляет данные задачи по его id. Возвращает обновлённый проект.

    Args:
        task_id: id задачи, которую нужно обновить.

        title: Заголовок задачи.

        description: Описание задачи.

        status: Статус задачи.

        project_id: Идентификатор проекта, к которому относится задача.

        assigned_user_id: Идентификатор пользователя, ответственного за выполнение задачи.

        due_date: Срок выполнения задачи.

    Returns:

        Обновлённая задача.
    """
    updated_task: TaskRead = await task_service.update_task(
        task_id,
        TaskUpdate(
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            project_id=project_id,
            assigned_user_id=assigned_user_id,
        ),
    )
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
) -> None:
    """
    **Удаление задачи.**

    Удаляет данные о задаче по её id.

    Args:
        task_id: id задачи которого нужно удалить.

        task_service: Сервис управляющий задачами.

    """
    result = await task_service.delete_task(task_id)
