"""
DAO (Data Access Object) для работы с пользователями в базе данных.

Содержит методы для создания, поиска и обновления пользователей.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.dao.base import BaseDAO
from src.databases.sqlite.models import User


class UserDAO(BaseDAO):
    """DAO для модели `User`."""

    model = User

    @classmethod
    async def create_user(
        cls,
        session: AsyncSession,
        telegram_id: int,
        first_name: str,
        username: str | None = None,
    ) -> User:
        """
        Создает нового пользователя.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            telegram_id: Уникальный ID пользователя в Telegram.
            first_name: Имя пользователя.
            username: Никнейм пользователя (может быть None).

        Returns:
            Новый экземпляр модели User.
        """
        return await cls.add(
            session, telegram_id=telegram_id, first_name=first_name, username=username
        )

    @classmethod
    async def get_user_by_telegram_id(
        cls, session: AsyncSession, telegram_id: int
    ) -> User | None:
        """
        Находит пользователя по его Telegram ID.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            telegram_id: Уникальный ID пользователя в Telegram.

        Returns:
            Экземпляр модели User или None, если пользователь не найден.
        """
        # Используем существующий метод BaseDAO, предполагая, что telegram_id уникален
        # Или напишем специфичный запрос
        query = select(cls.model).where(cls.model.telegram_id == telegram_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
