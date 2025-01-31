from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models import Base
from app.api.schemas.project_schema import ProjectRead


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())

    tasks = relationship("Task", back_populates="project")
    members = relationship("User", secondary="user_projects", back_populates="projects")

    def to_read_model(self):
        return ProjectRead(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
        )
