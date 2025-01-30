import datetime
from typing import Any, Dict

import jwt

from app.core import app_config


class AuthJWTService:
    """
    Сервис для работы с JWT-токенами.
    """

    def __init__(self):
        """Инициализация сервиса с загрузкой ключей и алгоритма шифрования."""
        self.__private_key: str = app_config.auth_jwt.private_key_path.read_text()
        self._public_key: str = app_config.auth_jwt.public_key_path.read_text()
        self._algorithm: str = app_config.auth_jwt.algorithm
        self._expire_minutes: int = app_config.auth_jwt.expire_minutes

    def encode_jwt(self, payload: Dict[str, Any]) -> str:
        """
        Кодирование данных в JWT-токен.
        Args:
            payload: Данные для кодирования.
        Returns:
            str: Сформированный JWT-токен.
        """
        now = datetime.datetime.now(datetime.UTC)
        payload.update(
            exp=now + datetime.timedelta(minutes=self._expire_minutes), iat=now
        )
        return jwt.encode(
            payload=payload, key=self.__private_key, algorithm=self._algorithm
        )

    def decode_jwt(self, jwt_code: str) -> Dict[str, Any]:
        """
        Декодирование JWT-токена.
        Args:
            jwt_code: Кодированный JWT-токен.
        Returns:
            Dict[str, Any]: Декодированные данные.
        """
        return jwt.decode(
            jwt=jwt_code, key=self._public_key, algorithms=[self._algorithm]
        )
