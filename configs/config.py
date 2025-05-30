from environs import Env

env = Env()
env.read_env()  # читает из .env и системных переменных

class Config:
    # --- Общие настройки ---
    APP_NAME: str = env.str("APP_NAME", "MyApp")
    ENV: str = env.str("ENV", "development")  # development, staging, production
    DEBUG: bool = env.bool("DEBUG", True)
    PORT: int = env.int("PORT", 8000)

    # --- Секреты и ключи (обязательные) ---
    SECRET_KEY: str = env.str("SECRET_KEY")
    JWT_SECRET: str = env.str("JWT_SECRET")

    # --- База данных ---
    DB_ENGINE: str = env.str("DB_ENGINE", "postgresql")
    DB_HOST: str = env.str("DB_HOST", "localhost")
    DB_PORT: int = env.int("DB_PORT", 5432)
    DB_NAME: str = env.str("DB_NAME")
    DB_USER: str = env.str("DB_USER")
    DB_PASSWORD: str = env.str("DB_PASSWORD")
    DB_SSL_MODE: str = env.str("DB_SSL_MODE", "prefer")

    # --- Кэширование (Redis) ---
    REDIS_URL: str = env.str("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD: str = env.str("REDIS_PASSWORD", None)

    # --- Docker ---
    DOCKER_ENV: str = env.str("DOCKER_ENV", "development")
    DOCKER_IMAGE_NAME: str = env.str("DOCKER_IMAGE_NAME", "myapp-image")
    DOCKER_CONTAINER_NAME: str = env.str("DOCKER_CONTAINER_NAME", "myapp-container")

    # --- Telegram Bot ---
    TELEGRAM_BOT_TOKEN: str = env.str("TELEGRAM_BOT_TOKEN", None)
    TELEGRAM_CHAT_ID: str = env.str("TELEGRAM_CHAT_ID", None)
    TELEGRAM_ADMIN_IDS: list[int] = [int(x) for x in env.list("TELEGRAM_ADMIN_IDS", [])]
    
    # --- Google API ---
    GOOGLE_API_KEY: str = env.str("GOOGLE_API_KEY", None)
    GOOGLE_CLIENT_ID: str = env.str("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET: str = env.str("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_REDIRECT_URI: str = env.str("GOOGLE_REDIRECT_URI", None)

    # --- Email настройки ---
    EMAIL_HOST: str = env.str("EMAIL_HOST", None)
    EMAIL_PORT: int = env.int("EMAIL_PORT", 587)
    EMAIL_HOST_USER: str = env.str("EMAIL_HOST_USER", None)
    EMAIL_HOST_PASSWORD: str = env.str("EMAIL_HOST_PASSWORD", None)
    EMAIL_USE_TLS: bool = env.bool("EMAIL_USE_TLS", True)
    EMAIL_USE_SSL: bool = env.bool("EMAIL_USE_SSL", False)
    EMAIL_DEFAULT_FROM: str = env.str("EMAIL_DEFAULT_FROM", None)

    # --- Sentry ---
    SENTRY_DSN: str = env.str("SENTRY_DSN", None)

    # --- Логирование ---
    LOG_LEVEL: str = env.str("LOG_LEVEL", "INFO")

    # --- API и внешние сервисы ---
    API_SERVICE_URL: str = env.str("API_SERVICE_URL", None)
    API_SERVICE_KEY: str = env.str("API_SERVICE_KEY", None)

    # --- Другие ---
    TIMEZONE: str = env.str("TIMEZONE", "UTC")
    MAX_WORKERS: int = env.int("MAX_WORKERS", 5)

    # --- Безопасность ---
    CORS_ALLOWED_ORIGINS: list = env.list("CORS_ALLOWED_ORIGINS", ["http://localhost"])
    SESSION_COOKIE_SECURE: bool = env.bool("SESSION_COOKIE_SECURE", False)
    CSRF_COOKIE_SECURE: bool = env.bool("CSRF_COOKIE_SECURE", False)


config = Config()
