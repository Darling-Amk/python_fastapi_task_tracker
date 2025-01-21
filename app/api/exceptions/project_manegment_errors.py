from .base import AppError


class ProjectConnectionNotFoundError(AppError):
    """Ошибка: Связь между пользователем и проектом не найдена"""

    def __init__(self, mes: str = "Связь между пользователем и проектом не существует"):
        super().__init__(
            message=mes,
            status_code=404,
        )


class ProjectConnectionAlreadyExist(AppError):
    """Ошибка: Связь между пользователем и проектом не найдена"""

    def __init__(self):
        super().__init__(
            message="Связь между пользователем и проектом уже существует",
            status_code=400,
        )
