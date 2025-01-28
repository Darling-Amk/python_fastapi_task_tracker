from pydantic import BaseModel, EmailStr


# Pydantic-схема для валидации данных пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserRead(BaseModel):
    id: int
    email: EmailStr | str
    name: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None

    class Config:
        from_attributes = True  # Включаем поддержку ORM
