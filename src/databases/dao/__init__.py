"""
Модуль для работы с DAO (Data Access Objects)
"""

from .base import BaseDAO
from .message_dao import MessageDAO
from .user_dao import UserDAO

__all__ = [
    "BaseDAO",
    "UserDAO",
    "MessageDAO",
]
