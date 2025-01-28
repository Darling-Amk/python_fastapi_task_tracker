from .base import AppError


class InvalidAuthError(AppError):
    """Неправильная почта или пароль."""

    def __init__(self):
        super().__init__(message="Неправильная почта или пароль", status_code=401)
