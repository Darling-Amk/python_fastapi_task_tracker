# app/models.py
import enum
from datetime import UTC, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.schemas.project_schema import ProjectRead
from app.api.schemas.projects_users_schems import ProjectUserRead
from app.api.schemas.user_schema import UserRead

Base = declarative_base()


# Enum для статуса задачи
class TaskStatus(str, enum.Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()

    projects = relationship(
        "Project", secondary="user_projects", back_populates="members"
    )

    def to_read_model(self):
        return UserRead(id=self.id, email=self.email, name=self.name)


# Модель проекта
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


# Модель задачи
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now(UTC))
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User")


# Таблица для связки пользователей и проектов (многие ко многим)
class UserProjects(Base):
    __tablename__ = "user_projects"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), primary_key=True)
