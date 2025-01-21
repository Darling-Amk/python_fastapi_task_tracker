from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class ProjectUpdate(BaseModel):
    name: str | None
    description: str | None

    class Config:
        from_attributes = True  # Включаем поддержку ORM
