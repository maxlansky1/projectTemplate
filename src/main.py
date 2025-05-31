# src/main.py
import sys
print("sys.path[0]:", sys.path[0])
import configs.config
print("Import worked")

from utils.logger import get_logger

# Настраиваем логирование
logger = get_logger(__name__)

def main():
    # Тестируем логгер
    logger.debug("А")
    logger.info("Б")
    logger.warning("В")
    logger.error("Г")
    logger.critical("Д")

    print("Это обычный print()")

if __name__ == "__main__":
    main()
