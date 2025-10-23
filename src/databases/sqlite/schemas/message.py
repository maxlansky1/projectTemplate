"""
Схемы Pydantic для сообщений чат-бота.

- `MessageRead` — схема для вывода данных сообщения.
- `MessageCreate` — схема для валидации данных при создании нового сообщения.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class MessageRead(BaseModel):
    """Схема для сериализации сообщения при чтении."""

    id: int
    user_id: int
    dialog_session_id: str
    role: str
    content: str
    timestamp: datetime
    message_type: str

    model_config = ConfigDict(
        from_attributes=True,  # Позволяет создавать схему из ORM-объектов
    )


class MessageCreate(BaseModel):
    """Схема для валидации данных при создании нового сообщения."""

    user_id: int
    dialog_session_id: str
    role: str
    content: str
    message_type: Literal["text", "voice"] = (
        "text"  # Используем Literal для ограничения типа
    )
