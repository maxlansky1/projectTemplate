"""
Схемы Pydantic для пользователей чат-бота.

- `UserRead` — схема для вывода данных пользователя.
- `UserCreate` — схема для валидации данных при создании нового пользователя.
"""

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    """Схема для сериализации пользователя при чтении."""

    id: int
    telegram_id: int
    first_name: str
    username: str | None

    model_config = ConfigDict(
        from_attributes=True,  # Позволяет создавать схему из ORM-объектов
    )


class UserCreate(BaseModel):
    """Схема для валидации данных при создании нового пользователя."""

    telegram_id: int
    first_name: str
    username: str | None = None  # Поле может быть опциональным при создании
