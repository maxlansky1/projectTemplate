# Вариант структуры

src/
├── __init__.py
├── main.py                   # Точка входа: запуск бота, подключение диспетчера
├── logs/                     # Папка для файлов логов (если используются)
├── bot/                      # Логика Telegram-бота (aiogram)
│   ├── __init__.py
│   ├── dispatcher.py         # Инициализация диспетчера aiogram, подключение роутеров
│   ├── handlers/             # Обработчики событий (команды, сообщения)
│   │   ├── __init__.py
│   │   ├── start.py          # Обработчик команды /start
│   │   ├── message.py        # Обработка входящих сообщений (текст, голос, фото и т.п.)
│   │   ├── commands.py       # Обработчики команд: /new_chat, /stats, /reset
│   │   └── admin.py          # Обработчики команд для администраторов
│   ├── filters/              # Кастомные фильтры aiogram (IsAdmin, IsModerator)
│   │   ├── __init__.py
│   │   ├── is_admin.py       # Фильтр: проверяет, является ли юзер админом
│   │   └── is_moder.py       # Фильтр: проверяет, является ли юзер модератором
│   ├── middlewares/          # Промежуточные обработчики (логирование, кэширование)
│   │   └── __init__.py
│   └── states.py             # FSM-состояния (например, выбор модели, ожидание ввода)
├── services/                 # Бизнес-логика (не зависит от aiogram)
│   ├── __init__.py
│   ├── context_service.py    # Управление контекстом (чтение/запись в Redis/SQL)
│   ├── ai_service.py         # Интеграция с ИИ (например, вызов OpenAI/другого API)
│   ├── user_service.py       # Работа с юзерами (роли, сессии, создание/чтение)
│   └── stats_service.py      # Сбор и подсчёт статистики (кол-во юзеров, сообщений)
├── databases/                # Работа с базами данных (Redis и SQLite)
│   ├── __init__.py
│   ├── redis.py              # Подключение и вспомогательные функции для Redis
│   └── sqlite/               # Работа с SQLite через SQLAlchemy
│       ├── __init__.py
│       ├── connection.py     # Подключение к БД, создание сессии
│       ├── core.py           # Базовая модель, настройки SQLAlchemy
│       ├── models/           # ORM-модели (User, Message)
│       │   ├── __init__.py
│       │   ├── base.py       # Базовая модель SQLAlchemy
│       │   ├── user.py       # Модель пользователя
│       │   └── message.py    # Модель сообщения
│       ├── schemas/          # Pydantic-схемы для валидации (UserRead, MessageCreate)
│       │   ├── __init__.py
│       │   ├── user.py       # Схемы для юзера
│       │   └── message.py    # Схемы для сообщения
│       └── dao/              # Data Access Objects (CRUD-операции)
│           ├── __init__.py
│           ├── base.py       # Базовый DAO
│           ├── user_dao.py   # CRUD для юзера
│           └── message_dao.py # CRUD для сообщения
├── utils/                    # Вспомогательные утилиты (не зависят от основной логики)
│   ├── __init__.py
│   ├── logger.py             # Настройка логирования
│   └── helpers.py            # Вспомогательные функции (форматирование, конвертация)


## TODO: Реализация чат-бота с контекстом

### **Этап 1: Подготовка инфраструктуры**

- [ ] **Изменить структуру `src/`** (как в предыдущем ответе).
- [x] **Обновить `docker-compose.yaml`**: ОБСУДИТЬ ОТДЕЛЬНО
  - Добавить сервисы: `redis`.
  - Настроить порты, volumes, env.
- [ ] **Обновить `Dockerfile`**: ОБСУДИТЬ ОТДЕЛЬНО
  - Убедиться, что зависимости для `aiogram`, `redis` установлены.
- [x] **Обновить `requirements.txt`**
  ```
  aiogram
  redis
  ```

### **Этап 2: Настройка конфигурации**

- [x] **Обновить `configs/settings.py`**:
  - Добавить `DATABASE_URL`, `REDIS_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_IDS`.
- [x] **Обновить `configs/schemas/database.py`**:
  - Pydantic-модель для настроек БД.

### **Этап 3: Подключение баз данных**

- [x] **Создать `src/databases/redis.py`**:
  - Подключение к Redis через `redis.asyncio`.

### **Этап 4: ORM и DAO (SQLAlchemy)**

#### Таблица `users`

| Поле             | Тип данных        | Описание                                         | Ограничения/Индексы      |
| :--------------- | :---------------- | :----------------------------------------------- | :----------------------- |
| `id`             | `INTEGER`         | Уникальный идентификатор записи в БД.            | `PRIMARY KEY`, `AUTOINCREMENT` |
| `telegram_id`    | `INTEGER`         | Уникальный идентификатор пользователя в Telegram.| `UNIQUE`, `INDEX`        |
| `first_name`     | `TEXT`            | Имя пользователя из Telegram.                   |                          |
| `username`       | `TEXT` (Nullable) | Telegram-ник пользователя.                      |                          |
| `created_at`     | `DATETIME`        | Время создания записи.                          | `DEFAULT CURRENT_TIMESTAMP` |
| `updated_at`     | `DATETIME`        | Время последнего обновления записи.             | `DEFAULT CURRENT_TIMESTAMP`, `ON UPDATE CURRENT_TIMESTAMP` (или обновляется вручную SQLAlchemy) |

#### Таблица `messages`

| Поле               | Тип данных        | Описание                                                 | Ограничения/Индексы      |
| :----------------- | :---------------- | :------------------------------------------------------- | :----------------------- |
| `id`               | `INTEGER`         | Уникальный идентификатор сообщения.                      | `PRIMARY KEY`, `AUTOINCREMENT` |
| `user_id`          | `INTEGER`         | Ссылка на `id` пользователя в таблице `users`.          | `FOREIGN KEY`, `INDEX`   |
| `dialog_session_id`| `TEXT` (UUID)     | Уникальный идентификатор сессии диалога.                 | `INDEX`                  |
| `role`             | `TEXT`            | Роль персонажа в боте (например, "Dr_House", "Assistant").|                          |
| `content`          | `TEXT`            | Текст сообщения.                                         |                          |
| `timestamp`        | `DATETIME`        | Время отправки/создания сообщения.                       | `DEFAULT CURRENT_TIMESTAMP`, `INDEX` |
| `message_type`     | `TEXT`            | Тип сообщения (например, "text", "voice").              | `DEFAULT 'text'`         |


- [ ] **Создать `src/databases/sqlite/schemas/user.py`**:
  - Pydantic-схемы: `UserCreate`, `UserRead`.
- [ ] **Создать `src/databases/sqlite/schemas/message.py`**:
  - Pydantic-схемы: `MessageCreate`, `MessageRead`.
- [ ] **Создать `src/databases/sqlite/dao/user_dao.py`**:
  - CRUD: `create_user`, `get_user_by_telegram_id`.
- [ ] **Создать `src/databases/sqlite/dao/message_dao.py`**:
  - CRUD: `create_message`, `get_last_messages`, `get_all_messages_by_user`.

### **Этап 5: Сервисы**

- [ ] **Создать `src/services/user_service.py`**:
  - Получение/создание юзера в БД.
  - Проверка роли (юзер/админ).
- [ ] **Создать `src/services/context_service.py`**:
  - Добавление сообщения в Redis и БД.
  - Чтение контекста: сначала из Redis, если нет — из БД.
  - Управление TTL (24 часа).
- [ ] **Создать `src/services/ai_service.py`**:
  - Вызов ИИ (например, OpenRouter).
  - Передача контекста (последние 30 сообщений).
- [ ] **Создать `src/services/stats_service.py`**:
  - Подсчёт юзеров, сообщений, активности.

### **Этап 6: FSM и состояния**

- [ ] **Создать `src/bot/states.py`**:
  - FSM-состояния: `ChoosingMode`, `InDialog`, `Idle`.


### **Этап 7: Хендлеры (aiogram)**

- [ ] **Создать `src/bot/handlers/start.py`**:
  - Команда `/start`: приветствие, выбор роли.
- [ ] **Создать `src/bot/handlers/commands.py`**:
  - `/new_chat` — сброс контекста.
  - `/stats` — статистика (для админов).
- [ ] **Создать `src/bot/handlers/message.py`**:
  - Обработка текста: сохранить в Redis/БД, получить контекст, вызвать ИИ, ответить.
- [ ] **Создать `src/bot/handlers/admin.py`**:
  - Команды админов: `/ban`, `/stats`, `/broadcast`.
- [ ] **Создать `src/bot/handlers/setup_routers.py`**:
  - Собирает все роутеры.

---

### **Этап 8: Мидлвари (опционально, но желательно)**

- [ ] **Создать `src/bot/middlewares/context.py`**:
  - Мидлварь: автоматически читает/обновляет контекст.
- [ ] **Создать `src/bot/middlewares/stats.py`**:
  - Сбор статистики (юзер, сообщение, время).

---

### **Этап 9: Запуск и диспетчер**

- [ ] **Обновить `src/main.py`**:
  - Создание бота.
  - Подключение диспетчера (с Redis-стораджем).
  - Запуск поллинга.
- [ ] **Создать `src/bot/dispatcher.py`**:
  - Настройка `Dispatcher`, подключение хендлеров.

---

### **Этап 10: Миграции (Alembic)**

- [ ] **Настроить `alembic.ini`**
- [ ] **Создать миграции**:
  - `alembic revision --autogenerate -m "Create user and message tables"`.
  - `alembic upgrade head`.

---

### **Этап 11: Тестирование**

- [ ] **Запустить в Docker**.
- [ ] **Протестировать**:
  - `/start`, выбор роли.
  - Отправка сообщений.
  - Контекст (30 сообщений).
  - FSM.
  - Админка.

---

### **Этап 12: Логирование и мониторинг (дополнительно)**

- [ ] **Обновить `src/utils/logger.py`**:
  - Настроить логирование в файл и stdout.
- [ ] **(Опционально)** Добавить `Prometheus` + `Grafana`.

---

### **Этап 13: Деплой**

- [ ] **Обновить `.github/workflows/deploy_app.yml`**:
  - Автоматический деплой в Docker.
- [ ] **Настроить сервер** (например, VPS).
- [ ] **Запустить** `docker-compose up -d`.

---

### **Важные моменты**

- **Redis** — для кэша и FSM.
- **PostgreSQL** — для хранения всей истории.
- **FSM** — через `RedisStorage`.
- **Контекст** — 30 сообщений, TTL 24 часа.
- **Роли** — юзер, админ.
- **Сообщения** — юзер и бот.

---

### **TODO (отложенные задачи)**

- [ ] Флуд-контроль.
- [ ] Асинхронная очередь (например, Celery).
- [ ] Поддержка голосовых, фото, видео.
- [ ] Webhook (вместо поллинга).
- [ ] CI/CD улучшения.
- [ ] Миграция на PostgreSQL