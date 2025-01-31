from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.api.models import Base


# Таблица для связки пользователей и проектов (многие ко многим)
class UserProjects(Base):
    __tablename__ = "user_projects"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
