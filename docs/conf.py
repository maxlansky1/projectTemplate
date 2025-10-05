"""
Конфигурационный файл для сборщика документации Sphinx.

Этот файл содержит все настройки, необходимые для кастомизации входных и выходных данных Sphinx.
Он выполняется как код на Python во время сборки, при этом текущая директория устанавливается как директория конфигурации.
"""

import os
import sys

# Добавляет родительскую директорию в системный путь, чтобы Sphinx мог найти исходные модули
# Получаем путь к корню проекта и
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.insert(0, project_root)

# Отладка для системного пути
# print(f"[DEBUG] Adding to sys.path: {project_root}")

# Информация о проекте для документации
project = "projectTemplate"
copyright = "2025, maxlansky"
author = "maxlansky"
release = "0.1"


# ============================================================================
# НАСТРОЙКИ ГЕНЕРАЦИИ UML-ДИАГРАММ (PlantUML)
# ============================================================================

# Настройки для работы с PlantUML и рендеринга UML-диаграмм.
# В GitHub Actions используется путь /usr/local/bin/plantuml/plantuml.jar, а для Windows — C:\\plantuml\\plantuml.jar.
if "GITHUB_ACTIONS" in os.environ:
    plantuml = "java -jar /usr/local/bin/plantuml/plantuml.jar"
elif os.name == "nt":  # Для Windows
    plantuml = r"java -jar C:\plantuml\plantuml.jar"
else:
    raise OSError("Unsupported OS")

# Формат рендера диаграммы
plantuml_output_format = "svg_img"
plantuml_latex_output_format = "svg"


# ============================================================================
# РАСШИРЕНИЯ SPHINX
# ============================================================================

# Список расширений Sphinx
extensions = [
    # === Поддержка форматов ===
    "myst_parser",  # поддержка Markdown (.md)
    # === Автодокументация ===
    "sphinx.ext.autodoc",  # автодока из docstring'ов
    "sphinx.ext.viewcode",  # ссылки на исходники
    "autoclasstoc",  #  улучшенная документация классов
    "sphinx.ext.napoleon",  # Google/NumPy стиль docstring'ов
    # === Утилиты и вспомогательные расширения ===
    "sphinx.ext.coverage",  # проверяет покрытие документации
    "sphinx_copybutton",  # добавляет кнопку скопировать код в документацию
    "sphinx_togglebutton",  # позволяет создавать разворачиваемые списки
    # === Визуализация и темы ===
    "sphinxcontrib.plantuml",  # добавляет поддержку plantuml
    "sphinx_rtd_theme",  # переключает на красивую тему
    # === GitHub Pages ===
    "sphinx.ext.githubpages",  # позволяет использовать стили sphinx при хостинге доков на github pages
]

# ============================================================================
# НАСТРОЙКИ АВТОДОКУМЕНТАЦИИ
# ============================================================================

# === Настройки autodoc ===
autodoc_default_options = {
    "members": True,  # Показывать публичные элементы
    "undoc-members": True,  # Показывать недокументированные члены (а не скрывать!)
    "private-members": True,  # Показывать приватные методы (_method) (а не скрывать!)
    "special-members": True,  # Показывать специальные методы (__init__, __str__) (а не скрывать!)
    "inherited-members": True,  # Показывать унаследованные методы
    "show-inheritance": True,  # Показывать иерархию наследования
    "exclude-members": "__weakref__",  # Исключить конкретные элементы
}

# Настройка mock для autodoc - рекурсивно мокает все подмодули и классы (временно отключено)
# autodoc_mock_imports = [
#     'configs',
# ]

# Порядок элементов по исходному коду (естественнее для чтения)
autodoc_member_order = "bysource"
# Включать docstring класса + __init__ метода
autoclass_content = "both"
# Формат типов - короткий (чище выглядит)
autodoc_typehints_format = "short"
# Отображение типов в описании (удобнее для чтения)
autodoc_typehints = "description"

# === Настройки sphinx.ext.napoleon ===
napoleon_google_docstring = True
napoleon_numpy_docstring = False  # если используете только Google стиль
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_param = True

# === Настройки для myst_parser ===
myst_enable_extensions = [
    "amsmath",  # математика
    "colon_fence",  # ::: для блоков кода
    "deflist",  # определения
    "dollarmath",  # $...$ для математики
    "fieldlist",  # списки полей
    "html_admonition",  # HTML admonitions
    "html_image",  # HTML изображения
    "replacements",  # замены (c/o -> ©/®)
    "smartquotes",  # красивые кавычки
    "strikethrough",  # зачеркнутый текст
    "substitution",  # подстановки
    "tasklist",  # чекбоксы
]

myst_heading_anchors = 7  # автоматически генерирует ссылки на заголовки (все 7 уровней)


# ============================================================================
# ОБРАБОТКА ИСХОДНЫХ ФАЙЛОВ
# ============================================================================

# Настройки для обработки исходных файлов, шаблонов, исключений и вывода HTML
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".git",  # игнорировать .git
    ".venv",  # виртуальное окружение
    "venv",  # альтернативный вариант
    ".env",  # файлы env
    "*.pyc",  # скомпилированные Python файлы
    "*~",  # временные файлы
]

language = "ru"


# ============================================================================
# НАСТРОЙКИ HTML-ТЕМЫ
# ============================================================================

# Настройки темы
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    # === Селекторы версий и языков ===
    # Эти опции добавляют выпадающие списки (селекторы) в шапку темы для переключения между версиями документации и языками.
    "version_selector": True,  # Включает селектор версий. Sphinx ожидает наличие переменной `html_context['versions']` для заполнения списка.
    "language_selector": False,  # Выключает селектор языков. Если True, Sphinx ожидает `html_context['languages']`.
    # `flyout_display` управляет поведением меню с селекторами и кнопкой поиска.
    # "flyout_display": "attached",  # Значение по умолчанию. Меню отображается как прикреплённый выпадающий список. Других стандартных значений, кроме 'attached', тема обычно не предоставляет, 'hidden' - это гипотетическое значение для описания.
    # === Навигация ===
    # Эти опции влияют на отображение и поведение бокового навигационного меню.
    "prev_next_buttons_location": "bottom",  # Определяет, где отображаются кнопки "Следующая страница" / "Предыдущая страница"
    "collapse_navigation": True,  # Дерево навигации в боковой панели будет свернуто по умолчанию, кроме текущего раздела.
    "sticky_navigation": True,  # Боковая навигационная панель будет оставаться видимой при прокрутке
    "navigation_depth": 6,  # Максимальная глубина вложенности элементов в боковом меню
    "titles_only": False,  # True - нет подзаголовков в меню. False - есть подзаголовки.
    # === Визуальные настройки ===
    "style_nav_header_background": "#2980B9",  # Устанавливает цвет фона шапки навигационной панели в формате HEX.
}

# Настройки для истории изменений документации
html_context = {
    # === GitHub ===
    "github_user": "maxlansky",
    "github_repo": "projectTemplate",
    "github_version": "main",
    "display_github": True,
    # === Версии (только если реально планируешь версионирование) ===
    # 'current_version': release,  # автоматически из release
    # 'versions': {
    #     'latest': '/',  # текущая версия
    #     '0.1': '/0.1/',  # предыдущие версии
    # },
    # === Дополнительно (для Read the Docs и других хостингов) ===
    "source_type": "github",
    "source_user": "maxlansky",
    "source_repo": "projectTemplate",
    "source_version": "main",
    "source_suffix": ".rst",
}


# ============================================================================
# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JS)
# ============================================================================

# Подключаем кастомные CSS и JS файлы
html_static_path = ["_static"]

html_js_files = [
    "custom.js",
]

html_css_files = [
    "custom.css",
]


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ============================================================================

# Дополнительная конфигурация sphinx-git (опционально)
git_untracked_check = False
git_remote_name = "origin"
git_branch = "main"  # или 'master', в зависимости от твоей ветки

# === Настройки sphinx-togglebutton ===

# Настройка CSS-селектора для элементов
togglebutton_selector = ".toggle, .admonition.dropdown"

# Настройка текста подсказки
togglebutton_hint = "Развернуть"
togglebutton_hint_hide = "Свернуть"

# Поведение при печати. По умолчанию True (разворачивает все элементы)
togglebutton_open_on_print = True
