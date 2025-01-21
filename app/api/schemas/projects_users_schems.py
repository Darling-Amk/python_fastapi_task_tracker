from pydantic import BaseModel

from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.user_schema import UserRead


class ProjectUserCreate(BaseModel):
    user_id: int
    project_id: int

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class ProjectUserRead(BaseModel):
    project: ProjectRead
    user: UserRead

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class ProjectUsersRead(BaseModel):
    project: ProjectRead
    users: list[UserRead]

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class UserProjectsRead(BaseModel):
    user: UserRead
    projects: list[ProjectRead]

    class Config:
        from_attributes = True  # Включаем поддержку ORM
