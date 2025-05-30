import os

# Папки, которые нужно игнорировать
IGNORE_FOLDERS = {'.git', '__pycache__', '.venv', 'venv', '__pycache__'}
# Файлы, которые нужно игнорировать
IGNORE_FILES = set()

def print_tree(start_path, prefix=''):
    """Рекурсивно выводит структуру каталогов в виде дерева."""
    entries = sorted(os.listdir(start_path))
    
    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        is_last = i == len(entries) - 1

        if entry.startswith('.') and os.path.isdir(path):
            if entry in IGNORE_FOLDERS:
                continue
        
        if os.path.isfile(path) and entry in IGNORE_FILES:
            continue

        # Определяем символ для отображения ветки
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry}")

        # Рекурсия для подкаталогов
        if os.path.isdir(path):
            new_prefix = "    " if is_last else "│   "
            print_tree(path, prefix + new_prefix)

if __name__ == "__main__":
    project_root = os.getcwd()  # Текущая директория
    root_name = os.path.basename(project_root) + '/'

    print(root_name)
    print()
    print_tree(project_root)