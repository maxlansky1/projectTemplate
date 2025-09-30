# 🗄️ Работа с базами данных

Пакет `databases` предоставляет асинхронную работу с базами данных через **SQLAlchemy 2.0+**.  
В текущей версии реализована поддержка **SQLite**, но архитектура позволяет легко добавлять **Redis**, **PostgreSQL**, **векторные базы данных** и другие.

## 🧩 SQLite

### 🛠️ Конфигурация

Все настройки, связанные с базами данных, находятся в файле `configs/schemas/database.py`.

Класс `SQLiteSettings` отвечает за настройки подключения к SQLite:

```{eval-rst}
.. toggle:: Показать

   .. autoclass:: configs.schemas.database.SQLiteSettings
      :members:
```

Пример значений в `.env` файле:

```bash
# Подключение к SQLite
SQLITE_DATABASE_URL=sqlite+aiosqlite:///./data/db.sqlite3  # URL для подключения к SQLite (aiosqlite — асинхронный драйвер)
SQLITE_ECHO=false                                         # Включить/отключить логирование SQL-запросов (true/false)
SQLITE_POOL_PRE_PING=true                                 # Проверять соединение перед использованием (рекомендуется true)
SQLITE_EXPIRE_ON_COMMIT=false                             # Не устаревают объекты после commit (рекомендуется false для асинхронной сессии)
SQLITE_AUTOFLUSH=false                                    # Отключить автоматический flush (рекомендуется false при ручном управлении сессией)
SQLITE_POOL_SIZE=5                                        # Размер пула подключений к БД (количество постоянных соединений)
SQLITE_MAX_OVERFLOW=10                                    # Максимальное количество дополнительных соединений сверх пула
```

```{admonition} Важно
:class: warning
SQLite используется в основном для разработки и прототипирования. Для продакшена рекомендуется использовать PostgreSQL или другую серверную СУБД.
```

```{admonition} Примечание
:class: note
Папка `data/` создаётся автоматически при запуске приложения, если она не существует.
```

### 🧰 Создание движка и сессии

Файл `src/databases/sqlite/core.py` отвечает за:

- Создание **асинхронного движка** SQLAlchemy
- Определение **базового класса** для ORM-моделей
- Настройку **фабрики сессий** с параметрами из конфигурации

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../src/databases/sqlite/core.py
      :language: python
      :caption: src/databases/sqlite/core.py
```

#### Основные компоненты

- `Base` — базовый класс для всех ORM-моделей. От него наследуются все модели (например, `User`), чтобы SQLAlchemy могла их распознавать и использовать в миграциях и запросах.
- `engine` — асинхронный движок, через который приложение взаимодействует с базой данных. Настроен с параметрами из `settings.database.sqlite` (например, URL, размер пула, логирование).
- `async_session` — фабрика асинхронных сессий. Создаёт сессии для выполнения запросов к БД с учётом настроек пула и поведения транзакций.

#### Экспорт модуля

Файл `src/databases/sqlite/__init__.py` экспортирует основные компоненты для работы с SQLite:

```python
from .core import engine, async_session, Base
from .connection import get_db_session

__all__ = [
    "engine",
    "async_session",
    "get_db_session",
    "Base",
]
```

Это позволяет импортировать их напрямую:

```python
from src.databases.sqlite import engine, Base, get_db_session
```

### 🔄 Подключение сессии к приложению

Файл `src/databases/sqlite/connection.py` предоставляет асинхронный генератор сессии базы данных:

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../src/databases/sqlite/connection.py
      :language: python
      :caption: src/databases/sqlite/connection.py
```

Функция `get_db_session()` используется для получения сессии базы данных. Она обеспечивает:

- Автоматическое открытие сессии при её использовании
- Гарантированное закрытие сессии после завершения (даже при возникновении ошибки)
- Управление сессией через `async with` или как зависимость в FastAPI

Пример использования в FastAPI:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.sqlite.connection import get_db_session

async def get_user_list(db: AsyncSession = Depends(get_db_session)):
    # Работа с сессией
    pass
```

Пример использования вне FastAPI:

```python
from src.databases.sqlite.connection import get_db_session

async def some_database_operation():
    async for session in get_db_session():
        # Работа с сессией
        pass
```

```{admonition} Важно
:class: note
Этот подход позволяет избежать утечек соединений и упрощает управление транзакциями в асинхронных приложениях.
```

### 📊 ORM-модели

Файл `src/databases/sqlite/models/user.py` содержит пример ORM-модели пользователя:

```{eval-rst}
.. toggle:: Показать

   .. literalinclude:: ../src/databases/sqlite/models/user.py
      :language: python
      :caption: src/databases/sqlite/models/user.py
```

Модель `User` наследуется от `Base` и предоставляет:

- `id` — уникальный идентификатор пользователя (первичный ключ)
- `username` — уникальное имя пользователя (с индексом)
- `email` — уникальный email пользователя (с индексом)

Пример использования в запросах:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.databases.sqlite.models.user import User

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()
```

```{admonition} Примечание
:class: note
Это базовая модель. В реальных проектах могут потребоваться дополнительные поля, такие как дата регистрации, хэш пароля, роли и т.д.
```

#### 🧱 Добавление новых моделей

Чтобы добавить новую таблицу в базу данных, создайте **ORM-модель** в `src/databases/sqlite/models/`.

Пример: создадим модель `Post`:

```python
# src/databases/sqlite/models/post.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..core import Base

class Post(Base):
    """
    ORM-модель поста.
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"
```

#### 📦 Регистрация модели

Чтобы Alembic и приложение **видели** новую модель, добавьте её в `src/databases/sqlite/models/__init__.py`:

```python
from .user import User
from .post import Post  # ← добавляем импорт

__all__ = [
    "User",
    "Post",  # ← добавляем в экспорт
]
```

Теперь модель будет доступна для миграций.

#### 🧭 Генерация миграций

Если вы добавили или изменили модель, нужно **сгенерировать миграцию**:

```bash
# В корне проекта
alembic revision --autogenerate -m "Add Post model"
```

Затем примените миграцию:

```bash
alembic upgrade head
```

#### 🔄 Изменение существующей модели

Чтобы изменить существующую модель (например, добавить поле):

1. Добавьте новое поле в класс модели:

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # ← новое поле
```

2. Сгенерируйте миграцию:

```bash
alembic revision --autogenerate -m "Add is_active field to User"
```

3. Примените миграцию:

```bash
alembic upgrade head
```

#### 🧠 Подключение модели к модулю

Чтобы использовать модель в другом модуле (например, в `main.py` или в `services/`), импортируйте её:

```python
from src.databases.sqlite.models.user import User
from src.databases.sqlite.models.post import Post
```

Или через основной модуль:

```python
from src.databases.sqlite.models import User, Post
```

##### 🧪 Пример работы с моделью в сервисе

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.databases.sqlite.models import User

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()
```

#### 🧪 Тестирование модели

Чтобы протестировать новую модель, можно создать тест:

```python
# tests/test_models.py
import pytest
from src.databases.sqlite.models import User

def test_user_model():
    user = User(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"
```

#### 📌 Важные замечания

- Не забывайте **обновлять миграции** при изменении моделей
- Используйте `Mapped` и `mapped_column` из SQLAlchemy 2.0
- Модели должны наследоваться от `Base`, чтобы быть доступными для миграций
- Папка `data/` создаётся автоматически, но если вы используете другую БД — проверьте, что путь существует


### 🔗 Отношения между моделями

SQLAlchemy позволяет описывать **отношения (relationships)** между моделями, что упрощает работу с связанными данными.

#### 🔄 One-to-One (Один к одному)

Связь "один-к-одному" используется для разделения основной и дополнительной информации.  
Например, данные пользователя в `User`, а профиль в `Profile`.

##### Пример:

```python
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey
from ..core import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Связь один-к-одному с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,  # Указывает на связь один-к-одному
        lazy="joined"   # Подгружает данные сразу при запросе
    )

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bio: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Обратная связь
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        uselist=False
    )
```

```{admonition} Пояснение
:class: tip

- `uselist=False` — указывает, что это не список, а один объект.
- `back_populates` — позволяет получить доступ к связанному объекту с обеих сторон.
```

#### 🔄 One-to-Many / Many-to-One (Один ко многим / Многие к одному)

Часто используемая связь, например: один пользователь — много постов.

##### Пример:

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Один пользователь — много постов
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"  # Удаляет посты при удалении пользователя
    )

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Многие посты — к одному пользователю
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
```

```{admonition} Пояснение
:class: tip

- `user_id` — внешний ключ, соединяющий пост с пользователем.
- `cascade="all, delete-orphan"` — удаляет дочерние объекты при удалении родителя.
- `back_populates` — двусторонняя связь.
```

#### 🔄 Many-to-Many (Многие ко многим)

Для связей "многие-ко-многим" используется промежуточная таблица (ассоциация).  
Пример: пользователи и теги.

##### Пример:

```python
from sqlalchemy import Table, Column, Integer, ForeignKey

# Промежуточная таблица
user_tag_association = Table(
    "user_tags",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=user_tag_association,
        back_populates="users"
    )

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_tag_association,
        back_populates="tags"
    )
```

```{admonition} Пояснение
:class: tip

- `secondary` — указывает на промежуточную таблицу.
- `back_populates` — двусторонняя связь.
```

#### 🧪 Пример использования отношений

После определения связей, вы можете работать с ними как с атрибутами:

```python
# Получить пользователя и его посты
user = await db.execute(select(User).options(selectinload(User.posts)))
user_with_posts = user.scalar_one()

for post in user_with_posts.posts:
    print(post.title)

# Создать пост для пользователя
new_post = Post(title="Новый пост", content="Содержимое", user_id=user_with_posts.id)
db.add(new_post)
await db.commit()
```

```{admonition} Важно
:class: warning

- Не забывайте использовать `selectinload` или `joinedload` для оптимизации запросов и избежания N+1 проблемы.
- При использовании `cascade="all, delete-orphan"` дочерние объекты будут удалены автоматически.
```

### 🧭 Alembic

Для превращения описанных **ORM-моделей** в **реальные таблицы** в базе данных используется процесс **миграции**.  
Для этих целей используется инструмент **Alembic**, который позволяет:

- Управлять версиями схемы базы данных
- Отслеживать изменения
- Легко переносить изменения на разные среды (dev, prod)

#### 🚀 Инициализация Alembic

Для начала работы с Alembic выполните команду в корне проекта:

```bash
alembic init -t async alembic
```

Эта команда создаст:

- Директорию `alembic/` — содержит файлы миграций
- Файл `alembic.ini` — основная конфигурация Alembic

#### ⚙️ Настройка `alembic/env.py`

Чтобы Alembic мог взаимодействовать с вашей базой данных, нужно настроить файл `alembic/env.py`:

##### 1. Импорты

Добавьте импорты базового класса `Base` и ваших моделей:

```python
from src.databases.sqlite.core import Base
from src.databases.sqlite.models import User  # импортируйте все свои модели
```

##### 2. Подключение к БД

Укажите URL подключения к базе данных:

```python
from configs.settings import settings

# В config.set_main_option можно указать:
config.set_main_option("sqlalchemy.url", settings.database.sqlite.database_url)
```

##### 3. Метаданные

Укажите, где искать модели:

```python
target_metadata = Base.metadata
```

Полный пример `alembic/env.py`:

```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from src.databases.sqlite.core import Base
from src.databases.sqlite.models import User  # добавьте свои модели

# Загружаем настройки
from configs.settings import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем URL подключения
config.set_main_option("sqlalchemy.url", settings.database.sqlite.database_url)

target_metadata = Base.metadata

# остальной код оставляем без изменений
```

#### 🧪 Создание миграции

После настройки Alembic может автоматически **сгенерировать миграцию** на основе ваших моделей:

```bash
alembic revision --autogenerate -m "Add User model"
```

Alembic проанализирует модели и создаст файл миграции в `alembic/versions/`.

#### 🚀 Применение миграции

Чтобы применить миграцию и **создать таблицы** в базе данных:

```bash
alembic upgrade head
```

Это применит все миграции до последней версии.

Для применения конкретной миграции:

```bash
alembic upgrade <revision_id>
```

#### 🔄 Откат миграции

Для отката последней миграции:

```bash
alembic downgrade -1
```

Для отката до конкретной версии:

```bash
alembic downgrade <revision_id>
```

#### ⚠️ Особенности с ENUM

Если вы используете тип `ENUM` в PostgreSQL:

- Укажите `create_type=False` в колонке, чтобы Alembic не пытался повторно создать тип:

```python
gender: Mapped[GenderEnum] = mapped_column(
    Enum(GenderEnum, create_type=False),
    nullable=False
)
```

- В методе `downgrade()` вручную удалите типы:

```python
def downgrade() -> None:
    op.drop_table('users')
    # Удаление типов ENUM
    op.execute('DROP TYPE IF EXISTS genderenum')
```

```{admonition} Важно
:class: warning

- Всегда используйте `create_type=False` для ENUM в миграциях.
- Не забывайте удалять ENUM-типы при откате миграций.
```

```{admonition} Примечание
:class: note

Если вы используете SQLite, тип `ENUM` не поддерживается. Используйте `String` или `Integer` с валидацией на уровне приложения.
```

#### 🧩 Пример файла миграции

Созданный файл `alembic/versions/xxx_add_user_model.py` будет содержать:

```python
"""Add User model

Revision ID: xxx
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'xxx'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('users')
```

```{admonition} Пояснение
:class: tip

- `upgrade()` — применяет изменения (создаёт таблицы).
- `downgrade()` — откатывает изменения (удаляет таблицы).
```

## 🧠 Redis

## 🔍 VectorDB
