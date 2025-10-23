"""
Модуль для подключения к Redis и предоставления клиента.

Содержит:
- redis_client: глобальный асинхронный клиент Redis.
- get_redis_client: функцию для получения клиента (может быть использована как зависимость в FastAPI, если понадобится).
- setup_redis: асинхронную функцию для инициализации клиента при запуске приложения.
- close_redis: асинхронную функцию для закрытия клиента при завершении приложения.
"""

import redis.asyncio as redis
from redis.asyncio import Redis

from configs.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Глобальная переменная для клиента Redis
redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    """
    Возвращает глобальный асинхронный клиент Redis.

    Raises:
        RuntimeError: Если клиент Redis не был инициализирован.
    """
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call setup_redis first.")
    return redis_client


async def setup_redis() -> None:
    """
    Инициализирует асинхронный клиент Redis при запуске приложения.

    Использует настройки из `settings.database.redis`.
    """
    global redis_client
    redis_config = settings.database.redis

    try:
        # Создаём ConnectionPool с настройками из конфига
        # Пул соединений управляется самим клиентом
        pool = redis.ConnectionPool.from_url(
            url=redis_config.redis_url,
            db=redis_config.redis_db,
            decode_responses=redis_config.decode_responses,
            # max_connections=10,  # Пример: ограничить пул (настройте по необходимости)
            # retry_on_timeout=True, # Пример: повтор при таймауте
            # health_check_interval=30, # Пример: интервал проверки здоровья
        )

        # Инициализируем клиент с пулом
        redis_client = redis.Redis(
            connection_pool=pool,
            # socket_keepalive=True, # Пример дополнительной опции
        )
        # Проверяем подключение
        await redis_client.ping()
        logger.info("Redis client initialized and connection verified.")
    except redis.AuthenticationError:
        logger.error(
            "Redis authentication failed. Check REDIS_USER and REDIS_USER_PASSWORD."
        )
        raise
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while setting up Redis: {e}")
        raise


async def close_redis() -> None:
    """
    Закрывает соединение с Redis при завершении приложения.
    """
    global redis_client
    if redis_client:
        await redis_client.aclose()  # Используем aclose для асинхронного закрытия
        logger.info("Redis client closed.")
        redis_client = None
