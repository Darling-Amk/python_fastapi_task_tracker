from .base import AppError


class InvalidAuthError(AppError):
    """Неправильная почта или пароль."""

    def __init__(self):
        super().__init__(message="Неправильная почта или пароль", status_code=401)


class InvalidJWTPayloadError(AppError):
    """Ошибка в содержимом JWT токена"""

    def __init__(self):
        super().__init__(message="Ошибка в содержимом JWT токена", status_code=401)


class InvalidJWTError(AppError):
    """Невозможно декодировать токен"""

    def __init__(self):
        super().__init__(message="Невозможно декодировать токен", status_code=401)
