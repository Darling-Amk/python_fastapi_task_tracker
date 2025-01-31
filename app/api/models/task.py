from datetime import UTC, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models import Base
from app.api.models.task_status import TaskStatus
from app.api.schemas.task import TaskRead


# Модель задачи
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now(UTC))
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    assigned_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User")

    def to_read_model(self):
        return TaskRead(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            due_date=self.due_date,
            created_at=self.created_at,
            project_id=self.project_id,
            assigned_user_id=self.assigned_user_id,
        )
