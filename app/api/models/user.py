from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models import Base
from app.api.schemas.user_schema import UserRead


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[bytes] = mapped_column()
    name: Mapped[str] = mapped_column()

    projects = relationship(
        "Project", secondary="user_projects", back_populates="members"
    )

    def to_read_model(self):
        return UserRead(id=self.id, email=self.email, name=self.name)
