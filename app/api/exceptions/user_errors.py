from .base import AppError


class UserAlreadyExistsError(AppError):
    """Ошибка: пользователь с таким email уже существует."""
    def __init__(self):
        super().__init__(message="Пользователь с такой почтой уже существует", status_code=400)

class UserNotFoundError(AppError):
    """Ошибка: пользователь не найден."""
    def __init__(self):
        super().__init__(message="Пользователь не найден", status_code=404)
