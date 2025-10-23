"""
Модуль для импорта всех ORM-моделей SQLite.

Здесь регистрируются все модели, чтобы Alembic мог их видеть.
"""

from .message import Message  # Импортируем новую модель
from .user import User

__all__ = [
    "User",
    "Message",  # Добавляем новую модель в экспорт
]
