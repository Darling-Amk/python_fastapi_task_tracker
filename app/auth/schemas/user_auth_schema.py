from pydantic import BaseModel, EmailStr


# Pydantic-схема для валидации данных пользователя
class UserAuth(BaseModel):
    name: str
    id: int
    email: EmailStr | str
    password_hash: bytes
