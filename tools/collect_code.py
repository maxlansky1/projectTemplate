"""
Графическое приложение для выбора файлов проекта, объединения их содержимого
и копирования в буфер обмена. Использует библиотеку Tkinter для построения
дерева каталогов и взаимодействия с пользователем.

Основные возможности:
---------------------
- Просмотр файлов и папок в указанной директории проекта.
- Игнорирование служебных директорий и файлов (например, __pycache__, .pyc).
- Выбор отдельных файлов с помощью клика.
- Сбор и объединение содержимого выбранных файлов.
- Копирование объединённого текста в системный буфер обмена.
- Отображение уведомлений о результате действия.
- Возможность копирования дерева структуры проекта.
- Возможность копирования дерева + содержимого выбранных файлов.
- Кнопка "Сбросить все галочки" для очистки выбора файлов.
- Кнопка "Обновить дерево" для пересборки дерева при изменении файлов.

Использование
1. Откройте консоль Git Bash в виртуальном окружении вашего проекта в VS Code
2. Запустите приложение командой `python tools/collect_code.py &`
3. Выберите нужные файлы для объединения и нажмите кнопку "Скопировать файлы"
"""

import os
import tkinter as tk
from tkinter import ttk

# Папки, которые нужно игнорировать
IGNORE_FOLDERS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    # "_build",  # папка сборки Sphinx
    # "_static",  # Стили Sphinx
    # "_templates",  # Шаблоны Sphinx
    ".ruff_cache",
}

# Файлы и расширения, которые нужно игнорировать
IGNORE_FILES = {
    ".DS_Store",
    ".pyc",  # Скомпилированные Python-файлы
    ".pyo",
    ".pyd",
    ".mo",
    ".log",
    ".tmp",
    "~",  # Временные файлы редакторов
}


def should_ignore(name, is_dir):
    """Определяет, нужно ли игнорировать файл или директорию при выводе.

    Args:
        name (str): Имя файла или директории.
        is_dir (bool): Флаг, указывающий является ли элемент директорией.

    Returns:
        bool: True если элемент нужно игнорировать, False если нужно включить в вывод.
    """
    if is_dir:
        return name in IGNORE_FOLDERS
    else:
        # Игнорируем по имени или по расширению
        if name in IGNORE_FILES:
            return True
        _, ext = os.path.splitext(name)
        return ext in IGNORE_FILES or name.startswith(".")


def get_tree_structure(start_path, prefix=""):
    """Рекурсивно возвращает структуру каталогов в виде строки ASCII-дерева.

    Args:
        start_path (str): Путь к корневой директории для вывода.
        prefix (str): Префикс для отступов (используется при рекурсивных вызовах).

    Returns:
        str: Строковое представление дерева структуры.
    """
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return f"{prefix}└── [Нет доступа]\n"

    output_lines = []
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
        line = f"{prefix}{connector}{entry}" + ("/" if is_dir else "")
        output_lines.append(line)

        if is_dir:
            new_prefix = "    " if is_last else "│   "
            subdir_output = get_tree_structure(path, prefix + new_prefix)
            # Удаляем лишние пустые строки из подкаталогов
            output_lines.append(subdir_output.rstrip())

    return "\n".join(output_lines) + "\n"


# === Основной класс приложения ===


class CodeCollectorApp:
    """
    GUI-приложение для выбора файлов, объединения их содержимого
    и копирования в буфер обмена.
    Использует Tkinter для отображения дерева файлов.
    """

    def __init__(self, root, project_path="."):
        """
        Инициализация главного окна приложения.

        :param root: корневой объект Tkinter
        :param project_path: путь к проекту (по умолчанию — текущая директория)
        """
        self.root = root
        self.project_path = project_path
        self.selected_files = set()  # множество выбранных файлов
        self.tree_items = {}  # словарь: item_id -> {'path', 'type'}
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка интерфейса: дерево файлов, кнопки копирования, метка уведомления.
        """
        self.root.title("Сбор кода для отправки")
        self.root.geometry("700x600")  # Увеличили высоту и ширину под новые кнопки

        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Дерево файлов
        self.tree = ttk.Treeview(main_frame)
        self.tree.heading("#0", text="Файлы и папки", anchor=tk.W)
        self.tree.column("#0", width=600)

        # Прокрутка
        scrollbar = ttk.Scrollbar(
            main_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Настройка стиля для больших кнопок
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 11), width=20, anchor="center")

        # Кнопки
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Левый столбец: копирование
        left_frame = ttk.Frame(button_frame)
        left_frame.pack(side=tk.LEFT, padx=(0, 10))

        btn1 = ttk.Button(
            left_frame,
            text="📋 Скопировать файлы",
            command=self.collect_and_copy,
            style="Large.TButton",
        )
        btn1.pack(pady=3)

        btn2 = ttk.Button(
            left_frame,
            text="📁 Скопировать дерево",
            command=self.copy_tree,
            style="Large.TButton",
        )
        btn2.pack(pady=3)

        btn3 = ttk.Button(
            left_frame,
            text="📄 Дерево + файлы",
            command=self.copy_tree_and_files,
            style="Large.TButton",
        )
        btn3.pack(pady=3)

        # Правый столбец: управление
        right_frame = ttk.Frame(button_frame)
        right_frame.pack(side=tk.RIGHT, padx=(10, 0))

        btn4 = ttk.Button(
            right_frame,
            text="🧹 Сбросить чекбоксы",
            command=self.clear_all_selections,
            style="Large.TButton",
        )
        btn4.pack(pady=3)

        btn5 = ttk.Button(
            right_frame,
            text="🔄 Обновить дерево",
            command=self.refresh_tree,
            style="Large.TButton",
        )
        btn5.pack(pady=3)

        # Метка для уведомления (изначально скрыта)
        self.status_label = tk.Label(self.root, text="", fg="green", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Заполняем дерево
        self.populate_tree()

        # Привязываем одинарный клик к переключению выбора файла
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)

    def populate_tree(self):
        """
        Заполняет дерево файлами и папками из проекта.
        """
        root_node = self.tree.insert(
            "", "end", text=f"{os.path.basename(self.project_path)}", open=True
        )
        self.tree_items[root_node] = {"path": self.project_path, "type": "dir"}
        self._add_directory_contents(root_node, self.project_path)

    def refresh_tree(self):
        """Обновляет дерево файлов, сохраняя выбранные файлы, если они остались."""
        # Сохраняем пути выбранных файлов
        selected_paths = {
            self.tree_items[item_id]["path"] for item_id in self.selected_files
        }

        # Очищаем дерево
        self.tree.delete(*self.tree.get_children())
        self.tree_items.clear()
        self.selected_files.clear()

        # Пересобираем дерево
        self.populate_tree()

        # Повторно выделяем файлы, которые остались
        for item_id, data in self.tree_items.items():
            if data["type"] == "file" and data["path"] in selected_paths:
                self.selected_files.add(item_id)
                self.tree.item(item_id, text=f"{self.tree.item(item_id, 'text')} [✓]")

        self.show_status("Дерево обновлено.", "green")

    def _add_directory_contents(self, parent, path):
        """
        Рекурсивно добавляет содержимое директории в дерево.

        :param parent: родительский элемент в дереве
        :param path: путь к директории
        """
        try:
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)

                # Проверяем, нужно ли игнорировать файл/папку
                if should_ignore(entry, os.path.isdir(entry_path)):
                    continue

                if os.path.isdir(entry_path):
                    node = self.tree.insert(
                        parent, "end", text=f"[DIR] {entry}", open=False
                    )
                    self.tree_items[node] = {"path": entry_path, "type": "dir"}
                    # Рекурсивно добавляем содержимое
                    self._add_directory_contents(node, entry_path)
                else:
                    node = self.tree.insert(parent, "end", text=f"[FILE] {entry}")
                    self.tree_items[node] = {"path": entry_path, "type": "file"}

        except PermissionError:
            pass  # Игнорируем папки, к которым нет доступа

    def on_item_click(self, event):
        """
        Обработчик клика по элементу дерева.
        Переключает выбор файла (добавляет/удаляет из self.selected_files).
        """
        item_id = self.tree.identify_row(event.y)
        if item_id not in self.tree_items:
            return

        item = self.tree_items[item_id]

        # Работаем только с файлами
        if item["type"] == "file":
            if item_id in self.selected_files:
                # Убираем из выбора
                self.selected_files.remove(item_id)
                # Обновляем текст в дереве
                self.tree.item(
                    item_id, text=self.tree.item(item_id, "text").replace(" [✓]", "")
                )
            else:
                # Добавляем в выбор
                self.selected_files.add(item_id)
                # Обновляем текст в дереве
                self.tree.item(item_id, text=f"{self.tree.item(item_id, 'text')} [✓]")

    def clear_all_selections(self):
        """
        Снимает выбор со всех файлов.
        """
        for item_id in self.selected_files.copy():
            # Убираем галочку с файла в дереве
            self.tree.item(
                item_id, text=self.tree.item(item_id, "text").replace(" [✓]", "")
            )
        self.selected_files.clear()
        self.show_status("Все галочки сняты.", "green")

    def collect_and_copy(self):
        """
        Собирает содержимое выбранных файлов и копирует в буфер обмена.
        Показывает уведомление под кнопкой.
        """
        if not self.selected_files:
            self.show_status("Нет выбранных файлов.", "red")
            return

        collected = []
        for item_id in self.selected_files:
            data = self.tree_items[item_id]
            try:
                with open(data["path"], encoding="utf-8") as f:
                    content = f.read()
                collected.append(f"=== {data['path']} ===\n{content}\n")
            except Exception as e:
                print(f"Ошибка при чтении {data['path']}: {e}")

        full_text = "\n".join(collected)

        # Копируем в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(full_text)
        self.root.update()

        self.show_status(
            f"Содержимое {len(self.selected_files)} файла(ов) скопировано в буфер обмена.",
            "green",
        )

    def copy_tree(self):
        """Копирует структуру дерева проекта в буфер обмена."""
        root_name = os.path.basename(self.project_path) + "/"
        tree_output = f"{root_name}\n{get_tree_structure(self.project_path).rstrip()}\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(tree_output)
        self.root.update()
        self.show_status("Структура проекта скопирована в буфер обмена.", "green")

    def copy_tree_and_files(self):
        """Копирует дерево проекта + содержимое выбранных файлов."""
        root_name = os.path.basename(self.project_path) + "/"
        tree_output = f"{root_name}\n{get_tree_structure(self.project_path).rstrip()}\n"

        if not self.selected_files:
            full_output = tree_output
        else:
            files_content = []
            for item_id in self.selected_files:
                data = self.tree_items[item_id]
                try:
                    with open(data["path"], encoding="utf-8") as f:
                        content = f.read()
                    files_content.append(f"=== {data['path']} ===\n{content}\n")
                except Exception as e:
                    print(f"Ошибка при чтении {data['path']}: {e}")
            files_text = "\n".join(files_content)
            full_output = tree_output + "\n" + files_text

        self.root.clipboard_clear()
        self.root.clipboard_append(full_output)
        self.root.update()
        self.show_status(
            f"Структура проекта + {len(self.selected_files)} файл(ов) скопированы в буфер обмена.",
            "green",
        )

    def show_status(self, message, color):
        """
        Показывает уведомление на 3 секунды.
        """
        self.status_label.config(text=message, fg=color)
        self.root.after(3000, self.clear_status)  # Через 3 секунды очистить

    def clear_status(self):
        """
        Очищает текст уведомления.
        """
        self.status_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCollectorApp(root)
    root.mainloop()
