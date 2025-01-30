import logging
from typing import Dict, Any

from pydantic import EmailStr

from app.api.exceptions import InvalidJWTPayloadError
from app.auth.models.payload_dict import UserPayload
from app.auth.schemas.user_auth_schema import UserAuth


class PayloadService:
    """Сервис для валидации и обработки данных приходящих в виде payload."""

    @staticmethod
    def create_from_user_auth(user_schema: UserAuth) -> UserPayload:
        """Создает объект UserPayload из схемы UserAuth.
        Args:
            user_schema : Схема аутентификации пользователя.
        Returns:
            UserPayload: Объект данных пользователя.
        """
        return {
            "sub": str(user_schema.id),
            "id": user_schema.id,
            "name": user_schema.name,
            "email": user_schema.email,
        }

    @staticmethod
    def payload2user_payload(payload: Dict[str, Any]) -> UserPayload:
        """
        Преобразует словарь payload в объект UserPayload.
        Проверяет наличие обязательных ключей 'sub', 'name' и 'email'.
        Args:
            payload: Словарь с данными пользователя.
        Raises:
            KeyError: Если отсутствует хотя бы один из необходимых ключей.
        Returns:
            UserPayload: Объект данных пользователя.
        """
        user_id: int | None = payload.get("sub")
        name: str | None = payload.get("name")
        email: str | EmailStr | None = payload.get("email")

        if user_id is None or name is None or email is None:
            logging.error(
                f"Неправильный payload, нет подходящего ключа sub,name, email  в ({payload.keys()})"
            )
            raise InvalidJWTPayloadError()

        return {
            "sub": user_id,
            "name": name,
            "email": email,
        }
