import subprocess
from pathlib import Path

# Пути к корневой директории исходного кода и директории с диаграммами
SRC_DIR = Path(__file__).parent.parent / "src"
DIAGRAMS_DIR = Path(__file__).parent.parent / "diagrams"
OUTPUT_FILE = DIAGRAMS_DIR / "temp_containers.puml"

# Настройки отображения для файлов по расширениям:
# (Человеческое имя типа файла, имя спрайта PlantUML, тег в диаграмме)
EXT_SETTINGS = {
    ".py":     ("Python", "python", "code"),
    ".js":     ("JavaScript", "javascript", "code"),
    ".ts":     ("TypeScript", "typescript", "code"),
    ".json":   ("JSON", "json", "config"),
    ".yaml":   ("YAML", "yaml", "config"),
    ".yml":    ("YAML", "yaml", "config"),
    ".txt":    ("Text", "text", "docs"),
    ".md":     ("Markdown", "markdown", "docs"),
    ".ipynb":  ("Notebook", "jupyter", "notebook"),
    ".html":   ("HTML", "html", "web"),
    ".css":    ("CSS", "css", "web"),
}


def get_changed_files():
    """
    Получает список новых (неотслеживаемых) файлов в репозитории Git.
    
    Использует `git ls-files --others --exclude-standard`, чтобы найти
    добавленные, но не закоммиченные файлы, игнорируя игнорируемые.
    
    Returns:
        List[str]: Список путей к файлам (относительно корня проекта).
    """
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        stdout=subprocess.PIPE, text=True
    )
    return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]


def build_container_definitions(added_files):
    """
    Обрабатывает список добавленных файлов и возвращает определения ссылок
    и вложенных границ контейнеров для генерации PlantUML.

    Args:
        added_files (List[str]): Список новых файлов в проекте.

    Returns:
        Tuple[List[str], dict]: 
            - Список строк `!define` для vscode-ссылок;
            - Словарь с иерархией папок и файлов, для генерации Container_Boundary.
    """
    defines = []
    boundaries = {}

    for filepath in added_files:
        path = Path(filepath)

        # Пропускаем всё, что не в папке src или не существует на диске
        if not filepath.startswith("src/") or not path.exists():
            continue

        # Игнорируем служебные файлы Python
        if path.name == "__init__.py":
            continue

        ext = path.suffix.lower()
        file_type, sprite, tag = EXT_SETTINGS.get(ext, ("File", "file", "other"))

        # Получаем относительный путь от корня проекта
        path = path.resolve()
        rel_path = path.relative_to(SRC_DIR.parent.resolve())
        parts = rel_path.parts  # Пример: ('src', 'handlers', 'admin.py')

        # Создаём уникальные идентификаторы и ссылку для VSCode
        var_name = (path.stem + "_" + ext.lstrip(".")).lower()
        var_const = var_name.upper()
        vscode_link = f"vscode://file/C:/gleb/projects/projectTemplate/{rel_path.as_posix()}"
        defines.append(f'!define {var_const} "{vscode_link}"')

        # Построение иерархии папок: src/.../папка/файл
        current = boundaries
        for part in parts[1:-1]:  # Пропускаем "src", обходим папки
            current = current.setdefault(part, {})
        current.setdefault("files", []).append(
            (parts[-1], var_name, file_type, sprite, tag, var_const)
        )

    return defines, boundaries


def write_container_block(f, name, content, indent=0):
    """
    Рекурсивно записывает блок Container_Boundary и файлы внутри него.

    Args:
        f (file): Открытый файловый объект для записи.
        name (str): Название текущего блока.
        content (dict): Содержимое (вложенные папки и файлы).
        indent (int): Текущий уровень отступа (для форматирования).
    """
    space = " " * indent

    # Добавляем файлы, если есть
    if "files" in content:
        for filename, var_name, file_type, sprite, tag, var_const in content["files"]:
            f.write(f'{space}    Container({var_name}, "{filename}", "{file_type}", "[CHOOSE NAME]", $tags="{tag}", $sprite="{sprite}", $link={var_const})\n')

    # Рекурсивно обрабатываем подпапки
    for subfolder, subcontent in content.items():
        if subfolder == "files":
            continue
        f.write(f'{space}    Container_Boundary({subfolder}, "{subfolder}", $tags="code") {{\n')
        write_container_block(f, subfolder, subcontent, indent + 4)
        f.write(f'{space}    }}\n')


def write_temp_puml(defines, boundaries):
    """
    Генерирует временный .puml файл с определениями ссылок и иерархией компонентов.

    Args:
        defines (List[str]): Список !define для VSCode-ссылок.
        boundaries (dict): Иерархическая структура папок и файлов.
    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # Вставляем !define ссылки
        for line in defines:
            f.write(line + "\n")

        # Корневой блок Container_Boundary
        f.write("\nContainer_Boundary(src, \"src (исходный код)\", $tags=\"code\") {\n")
        write_container_block(f, "src", boundaries, indent=4)
        f.write("}\n")


if __name__ == "__main__":
    # Основной рабочий процесс при запуске как скрипта:
    # 1. Получаем новые файлы
    # 2. Строим структуру контейнеров
    # 3. Записываем временную диаграмму
    added_files = get_changed_files()
    defines, boundaries = build_container_definitions(added_files)
    write_temp_puml(defines, boundaries)
