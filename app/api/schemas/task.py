from datetime import datetime

from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class TaskRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class TaskUpdate(BaseModel):
    name: str | None
    description: str | None

    class Config:
        from_attributes = True  # Включаем поддержку ORM
