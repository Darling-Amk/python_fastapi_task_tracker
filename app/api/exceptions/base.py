

class AppError(Exception):
    """Базовый класс для всех кастомных ошибок."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def to_dict(self):
        return {"detail": self.message}