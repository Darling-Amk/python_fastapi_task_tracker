from .base import AppError


class ProjectNotFoundError(AppError):
    """Ошибка: проект не найден."""

    def __init__(self):
        super().__init__(message="Проект не найден", status_code=404)
