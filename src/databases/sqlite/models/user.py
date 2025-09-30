from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..core import Base


class User(Base):
    """
    ORM-модель пользователя.
    """

    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
