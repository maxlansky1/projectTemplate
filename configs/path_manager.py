"""Модуль path_manager предоставляет централизованный доступ ко всем ключевым путям проекта.

Все пути представлены как объекты Path из библиотеки pathlib для переносимости и удобства.
"""

import os
from pathlib import Path

# === Определение корня проекта ===
PROJECT_ROOT = Path(__file__).parent.parent


# === Базовые директории проекта ===
CONFIGS_DIR = PROJECT_ROOT / "configs"
DIAGRAMS_DIR = PROJECT_ROOT / "diagrams"
DOCS_DIR = PROJECT_ROOT / "docs"
LOGS_DIR = PROJECT_ROOT / "logs"
NOTES_DIR = PROJECT_ROOT / "notes"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
TOOLS_DIR = PROJECT_ROOT / "tools"


# === Файлы верхнего уровня ===
DOCKERFILE_PATH = PROJECT_ROOT / "Dockerfile"
MAKEFILE_PATH = PROJECT_ROOT / "Makefile"
README_PATH = PROJECT_ROOT / "README.md"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"
DOCKER_COMPOSE_PATH = PROJECT_ROOT / "docker-compose.yaml"
GITHUB_WORKFLOWS_DIR = PROJECT_ROOT / ".github" / "workflows"


# === Поддиректории src/ ===
SRC_UTILS_DIR = SRC_DIR / "utils"
SRC_API_DIR = SRC_DIR / "api"
SRC_DB_DIR = SRC_DIR / "db"
SRC_LOGS_DIR = SRC_DIR / "logs"
MAIN_PY_PATH = SRC_DIR / "main.py"


# === Конкретные файлы проекта ===
CONFIG_PY_PATH = CONFIGS_DIR / "config.py"
PATH_MANAGER_PY_PATH = CONFIGS_DIR / "path_manager.py"

PROJECT_STRUCTURE_PUML_PATH = DIAGRAMS_DIR / "project_structure.puml"
PROJECT_STRUCTURE_SVG_PATH = DIAGRAMS_DIR / "project_structure.svg"
TEMP_CONTAINERS_PUML_PATH = DIAGRAMS_DIR / "temp_containers.puml"

TEST_MAIN_PY_PATH = TESTS_DIR / "test_main.py"

DIAGRAM_AUTO_UPDATE_SCRIPT = TOOLS_DIR / "diagram_auto_update.py"
PRINT_STRUCTURE_SCRIPT = TOOLS_DIR / "print_structure.py"


# === Переменные окружения для переопределения путей (опционально) ===
LOGS_DIR_ENV = os.getenv("PROJECT_LOGS_DIR")
if LOGS_DIR_ENV:
    LOGS_DIR = Path(LOGS_DIR_ENV)


# === Функция проверки и создания ключевых директорий ===
def ensure_directories():
    """Создаёт необходимые директории, если они отсутствуют.

    Выводит информационное сообщение в stdout.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Убедились, что существует директория: {LOGS_DIR}")


# === Функция вывода всех известных путей ===
def print_project_paths():
    """Выводит все определённые пути в терминал для дебага и проверки.

    Outputs:
        Выводит в stdout список всех путей, определённых как глобальные переменные
        в верхнем регистре, которые являются экземплярами Path.

    Format:
        Вывод включает разделители "===" перед и после списка путей.
    """
    print("\n=== Project Paths ===")
    for name, value in globals().items():
        if isinstance(value, Path) and name.isupper():
            print(f"{name} = {value}")
    print("=====================")


# === Если запускается как скрипт — выводим все пути ===
if __name__ == "__main__":
    print_project_paths()
    ensure_directories()
