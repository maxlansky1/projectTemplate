"""
ORM-модель пользователя для ролевого чат-бота.

Содержит поля:
- telegram_id: уникальный идентификатор пользователя в Telegram
- first_name: имя пользователя из Telegram
- username: Telegram-ник пользователя (может быть None)
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """
    ORM-модель пользователя.
    """

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    username: Mapped[str | None] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, first_name='{self.first_name}', username='{self.username}')>"
