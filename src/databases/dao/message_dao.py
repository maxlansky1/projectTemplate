"""
DAO (Data Access Object) для работы с сообщениями в базе данных.

Содержит методы для создания, поиска и удаления сообщений.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.dao.base import BaseDAO
from src.databases.sqlite.models import Message


class MessageDAO(BaseDAO):
    """DAO для модели `Message`."""

    model = Message

    @classmethod
    async def create_message(
        cls,
        session: AsyncSession,
        user_id: int,
        dialog_session_id: str,
        role: str,
        content: str,
        message_type: str = "text",
    ) -> Message:
        """
        Создает новое сообщение.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            user_id: ID пользователя, отправившего сообщение.
            dialog_session_id: ID сессии диалога.
            role: Роль в сообщении.
            content: Содержание сообщения.
            message_type: Тип сообщения (по умолчанию 'text').

        Returns:
            Новый экземпляр модели Message.
        """
        return await cls.add(
            session,
            user_id=user_id,
            dialog_session_id=dialog_session_id,
            role=role,
            content=content,
            message_type=message_type,
        )

    @classmethod
    async def get_last_messages(
        cls, session: AsyncSession, dialog_session_id: str, limit: int = 30
    ) -> list[Message]:
        """
        Получает последние N сообщений для указанной сессии диалога.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            dialog_session_id: ID сессии диалога.
            limit: Максимальное количество сообщений для возврата (по умолчанию 30).

        Returns:
            Список сообщений, отсортированных по времени в порядке убывания.
        """
        query = (
            select(cls.model)
            .where(cls.model.dialog_session_id == dialog_session_id)
            .order_by(cls.model.timestamp.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        # Возвращаем в прямом порядке (от старых к новым), так как инвертировали при выборке
        return result.scalars().all()[::-1]

    @classmethod
    async def get_all_messages_by_user(
        cls, session: AsyncSession, user_id: int
    ) -> list[Message]:
        """
        Получает все сообщения для указанного пользователя.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            user_id: ID пользователя.

        Returns:
            Список всех сообщений пользователя.
        """
        query = select(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_messages_by_session(
        cls, session: AsyncSession, dialog_session_id: str
    ) -> list[Message]:
        """
        Получает все сообщения для указанной сессии диалога.

        Args:
            session: Асинхронная сессия SQLAlchemy.
            dialog_session_id: ID сессии диалога.

        Returns:
            Список всех сообщений в сессии.
        """
        query = select(cls.model).where(
            cls.model.dialog_session_id == dialog_session_id
        )
        result = await session.execute(query)
        return result.scalars().all()
