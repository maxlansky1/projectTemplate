"""
Инициализация моделей конфигурации
"""

from src.utils.logger import get_logger

from .ai import AssemblyAISettings, ElevenLabsSettings, OpenRouterSettings
from .base import BaseConfig
from .file_processing import MediaProcessingSettings
from .storage import StorageSettings
from .telegram import TelegramSettings

logger = get_logger(__name__)

__all__ = [
    "BaseConfig",
    "TelegramSettings",
    "OpenRouterSettings",
    "AssemblyAISettings",
    "ElevenLabsSettings",
    "StorageSettings",
    "MediaProcessingSettings",
    "SQLiteSettings",
]

logger.debug("Конфигурационные модели загружены")
