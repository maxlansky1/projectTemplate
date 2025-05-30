import os

# Папки, которые нужно игнорировать
IGNORE_FOLDERS = {'.git', '__pycache__', '.venv', 'venv'}

# Файлы и расширения, которые нужно игнорировать
IGNORE_FILES = {
    '.DS_Store',
    '.pyc',        # Скомпилированные Python-файлы
    '.pyo',
    '.pyd',
    '.mo',
    '.log',
    '.tmp',
    '~',           # Временные файлы редакторов
}

def should_ignore(name, is_dir):
    """Определяет, нужно ли игнорировать элемент."""
    if is_dir:
        return name in IGNORE_FOLDERS
    else:
        # Игнорируем по имени или по расширению
        if name in IGNORE_FILES:
            return True
        _, ext = os.path.splitext(name)
        return ext in IGNORE_FILES or name.startswith('.')
    return False

def print_tree(start_path, prefix=''):
    """Рекурсивно выводит структуру каталогов в виде дерева."""
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        print(f"{prefix}└── [Нет доступа]")
        return

    filtered_entries = []
    for entry in entries:
        full_path = os.path.join(start_path, entry)
        is_dir = os.path.isdir(full_path)
        if not should_ignore(entry, is_dir):
            filtered_entries.append((entry, is_dir))

    for i, (entry, is_dir) in enumerate(filtered_entries):
        path = os.path.join(start_path, entry)
        is_last = i == len(filtered_entries) - 1

        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry}" + ('/' if is_dir else ''))

        if is_dir:
            new_prefix = "    " if is_last else "│   "
            print_tree(path, prefix + new_prefix)

if __name__ == "__main__":
    project_root = os.getcwd()  # Текущая директория
    root_name = os.path.basename(project_root) + '/'

    print(root_name)
    print()
    print_tree(project_root)