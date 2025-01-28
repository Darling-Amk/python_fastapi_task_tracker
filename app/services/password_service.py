import bcrypt


class PasswordService:
    """
    Класс для работы с паролями.
    """

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Хэширует пароль с использованием соли.
        Args:
            password: Пароль, который нужно захешировать.
        Returns:
            bytes: Хешированный пароль.
        """
        # Генерация уникальной соли
        salt = bcrypt.gensalt()
        # Хеширование пароля с солью
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        """
        Проверяет соответствие хеша паролю.
        Args:
            password: Исходный пароль.
            hashed_password: Хешированный пароль.
        Returns:
            bool: True, если пароль соответствует хешу, иначе False.
        """
        # Проверка соответствия пароля хешу
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
