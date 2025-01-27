from .base import AppError


class TaskNotFoundError(AppError):
    """Ошибка: задача не найдена."""

    def __init__(self):
        super().__init__(message="Задача не найдена", status_code=404)
