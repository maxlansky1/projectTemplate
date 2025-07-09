"""
Точка входа — главный запуск приложения.

Этот модуль содержит точку входа в приложение и вызывает основную функцию main().
"""

from src.utils.logger import get_logger

# Настраиваем логирование
logger = get_logger(__name__)


def main():
    """
    Запускает приложение.

    Логирует сообщения разных уровней и выводит тестовый текст через print().
    """

    logger.debug("А")
    logger.info("Б")
    logger.warning("В")
    logger.error("Г")
    logger.critical("Д")

    print("Это обычный print()")


if __name__ == "__main__":
    main()
