"""
ORM-модель сообщения для ролевого чат-бота.

Содержит поля:
- user_id: ссылка на пользователя
- dialog_session_id: идентификатор сессии диалога
- role: роль персонажа в сообщении
- content: текст сообщения
- message_type: тип сообщения (например, text, voice)
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Message(Base):
    """
    ORM-модель сообщения.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    dialog_session_id: Mapped[str] = mapped_column(
        String, index=True
    )  # Можно использовать UUID, если будете генерировать UUID в Python
    role: Mapped[str] = mapped_column(String)  # Роль персонажа
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), index=True
    )  # Используем UTC
    message_type: Mapped[str] = mapped_column(String, default="text")  # Тип сообщения

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, dialog_session_id={self.dialog_session_id}, role='{self.role}', timestamp={self.timestamp}, message_type='{self.message_type}')>"
