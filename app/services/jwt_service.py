from typing import Any, Dict

import jwt

from app.core import app_config


class AuthJWTService:
    """
    Сервис для работы с JWT-токенами.
    """

    def __init__(self):
        """Инициализация сервиса с загрузкой ключей и алгоритма шифрования."""
        private_key_path = app_config.auth_jwt.private_key_path
        public_key_path = app_config.auth_jwt.public_key_path
        self._private_key = private_key_path.read_text() if private_key_path else None
        self._public_key = public_key_path.read_text() if public_key_path else None
        self._algorithm = app_config.auth_jwt.algorithm

    def encode_jwt(self, payload: Dict[str, Any]) -> str:
        """
        Кодирование данных в JWT-токен.
        Args:
            payload: Данные для кодирования.
        Raises:
            ValueError: Если ключ или алгоритм не определены.
        Returns:
            str: Сформированный JWT-токен.
        """
        if not self._private_key or not self._algorithm:
            raise ValueError("Private key or algorithm is not defined.")
        return jwt.encode(
            payload=payload, key=self._private_key, algorithm=self._algorithm
        )

    def decode_jwt(self, jwt_code: str) -> Dict[str, Any]:
        """
        Декодирование JWT-токена.
        Args:
            jwt_code: Кодированный JWT-токен.
        Raises:
            ValueError: Если публичный ключ или алгоритм не определены.
        Returns:
            Dict[str, Any]: Декодированные данные.
        """
        if not self._public_key or not self._algorithm:
            raise ValueError("Public key or algorithm is not defined.")
        return jwt.decode(jwt=jwt_code, key=self._public_key, algorithm=self._algorithm)
