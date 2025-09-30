"""
Модуль для создания асинхронного движка и сессии SQLAlchemy.

Этот модуль настраивает подключение к базе данных SQLite с использованием
асинхронного движка SQLAlchemy. Он предоставляет все необходимые компоненты
для работы с базой данных в асинхронном режиме:

- `Base` — базовый класс для всех ORM-моделей, от которого наследуются
  все таблицы в базе данных. Используется для автоматического создания
  миграций и связывания моделей с таблицами в БД. Включает универсальные
  колонки: id, created_at, updated_at.

- `engine` — асинхронный движок, который управляет подключением к базе данных.
  Он отвечает за создание соединений, настройку пула соединений, логирование
  SQL-запросов и другие параметры подключения. Настроен с использованием
  параметров из конфигурации приложения (configs.settings).

- `async_session` — фабрика асинхронных сессий, которая создает сессии
  для выполнения запросов к базе данных. Сессия — это основной интерфейс
  для взаимодействия с БД в SQLAlchemy: добавление, изменение, удаление
  и выборка записей.

Путь к файлу базы данных формируется из настроек хранилища (settings.storage.data_dir)
и автоматически создается в папке /data при запуске приложения.
"""

from datetime import datetime
from pathlib import Path

from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from configs.settings import settings


# Базовый класс для всех ORM-моделей
class Base(DeclarativeBase):
    __abstract__ = True  # Не создает таблицу в БД

    # Универсальные колонки для всех моделей
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Автоматически формирует имя таблицы: User -> users, Post -> posts
        return cls.__name__.lower() + "s"


# Формируем путь и URL для подключения к БД
db_path: Path = settings.storage.data_dir / "db.sqlite3"
db_url: str = f"sqlite+aiosqlite:///{db_path}"


# Асинхронный движок с настройками из конфига
engine = create_async_engine(
    url=db_url,  # URL подключения к базе данных
    echo=settings.database.sqlite.echo,  # Логирование SQL-запросов
    pool_pre_ping=settings.database.sqlite.pool_pre_ping,  # Проверка соединения перед использованием
    pool_size=settings.database.sqlite.pool_size,  # Размер пула соединений
    max_overflow=settings.database.sqlite.max_overflow,  # Максимальное количество дополнительных соединений
)


# Фабрика асинхронных сессий
async_session = async_sessionmaker(
    engine,  # Движок, из которого создаются соединения
    expire_on_commit=settings.database.sqlite.expire_on_commit,  # Если True — объекты устаревают после commit
    autoflush=settings.database.sqlite.autoflush,  # Если True — автоматически синхронизирует изменения с БД
)
