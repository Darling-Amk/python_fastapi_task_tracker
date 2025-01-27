from datetime import datetime

from pydantic import BaseModel

from app.api.models.task_status import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime
    due_date: datetime
    project_id: int
    assigned_user_id: int

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    due_date: datetime
    project_id: int
    assigned_user_id: int

    class Config:
        from_attributes = True  # Включаем поддержку ORM


class TaskUpdate(BaseModel):
    title: str | None
    description: str | None
    status: TaskStatus | None
    due_date: datetime | None
    project_id: int | None
    assigned_user_id: int | None

    class Config:
        from_attributes = True  # Включаем поддержку ORM
