from fastapi import APIRouter, Depends

# from app.core.dependencies import get_task_service

router = APIRouter()
#
#
# @router.get("/")
# async def get_tasks(
#     task_service: TaskService = Depends(get_task_service),
# ) -> list[TaskRead]:
#     """
#     **Получение список всех задач.**
#
#     Returns:
#
#         Список задач.
#     """
#     tasks: list[TaskRead] = await task_service.get_tasks()
#     return tasks


#
#
# @router.post("/")
# async def create_task(
#     task_data: TaskCreate,
#     task_service: TaskService = Depends(get_task_service),
# ) -> TaskRead:
#     """
#     **Создание нового проекта.**
#
#     Args:
#
#         task_data: Данные для создания проекта.
#
#         task_service: Сервис управляющий проектами.
#
#
#     Returns:
#
#         Ответ с id созданного проекта.
#     """
#
#     new_task: TaskRead = await task_service.create_task(task_data)
#     return new_task
#
#
# @router.get("/{task_id}")
# async def get_task(
#     task_id: int,
#     task_service: TaskService = Depends(get_task_service),
# ) -> TaskRead:
#     """
#     **Получить проект по его id.**
#
#     Args:
#
#         task_id: id проекта, который необходимо получить.
#
#         task_service: Сервис управляющий проектами.
#
#     Returns:
#
#        Ответ с данными проекта или None, если проект не найден.
#     """
#
#     task: TaskRead = await task_service.get_task(task_id)
#     return task
#
#
# @router.put("/{task_id}")
# async def update_task(
#     task_id: int,
#     task_data: TaskUpdate,
#     task_service: TaskService = Depends(get_task_service),
# ) -> TaskRead:
#     """
#     **Обновление информации о проекте.**
#
#     Обновляет данные проекта по его id. Возвращает обновлённый проект.
#
#     Args:
#         task_id: id проекта, которого нужно обновить.
#
#         task_data: Данные, которые необходимо обновить.
#
#         task_service: Сервис управляющий проектами.
#
#
#     Returns:
#
#         Обновлённый проект.
#     """
#     updated_task: TaskRead = await task_service.update_task(task_id, task_data)
#     return updated_task
#
#
# @router.delete("/{task_id}")
# async def delete_task(
#     task_id: int,
#     task_service: TaskService = Depends(get_task_service),
# ) -> None:
#     """
#     **Удаление проекта.**
#
#     Удаляет данные о проекте по его id.
#
#     Args:
#         task_id: id проекта которого нужно удалить.
#
#         task_service: Сервис управляющий проектами.
#
#
#     Returns:
#
#         Обновлённый проект.
#     """
#     result = await task_service.delete_task(task_id)
