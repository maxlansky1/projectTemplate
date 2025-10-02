"""
Конфигурационный файл для сборщика документации Sphinx.

Этот файл содержит все настройки, необходимые для кастомизации входных и выходных данных Sphinx.
Он выполняется как код на Python во время сборки, при этом текущая директория устанавливается как директория конфигурации.
"""

import os
import sys

# Добавляет родительскую директорию в системный путь, чтобы Sphinx мог найти исходные модули
# для автодокументации. Это позволяет Sphinx импортировать модули проекта из корневой директории.
sys.path.insert(0, os.path.abspath(".."))

# Информация о проекте для документации
project = "projectTemplate"
copyright = "2025, maxlansky"
author = "maxlansky"
release = "0.1"

# [ ] TODO: Добавить версионирование документации


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

plantuml_output_format = "svg"
plantuml_latex_output_format = "svg"


# ============================================================================
# РАСШИРЕНИЯ SPHINX
# ============================================================================

# TODO: внедрить https://github.com/sphinx-contrib/multiversion для версионирования документации
# TODO:внедрить https://autoclasstoc.readthedocs.io/ для улучшенной документации классов
# TODO: внедрить https://sphinx-hoverxref.readthedocs.io/en/latest/ для интерактивных подсказок в документации

# Список расширений Sphinx
extensions = [
    # === Поддержка форматов ===
    "myst_parser",  # поддержка Markdown (.md)
    # === Автодокументация ===
    "sphinx.ext.autodoc",  # автодока из docstring'ов
    "sphinx.ext.viewcode",  # ссылки на исходники
    "sphinx.ext.napoleon",  # Google/NumPy стиль docstring'ов
    "sphinx_autodoc_typehints",  # type hints в сигнатурах
    # === Утилиты и вспомогательные расширения ===
    "sphinx.ext.todo",  # поддержка TODO
    "sphinx.ext.coverage",  # проверяет покрытие документации
    "sphinx.ext.ifconfig",  # условные директивы в документации
    "sphinx_copybutton",  # добавляет кнопку скопировать код в документацию
    "sphinx_togglebutton",  # позволяет создавать разворачиваемые списки
    # === Визуализация и темы ===
    "sphinxcontrib.plantuml",  # добавляет поддержку plantuml
    "sphinx_rtd_theme",  # переключает на красивую тему
    # === GitHub Pages ===
    "sphinx.ext.githubpages",  # позволяет использовать стили sphinx при хостинге доков на github pages
]

# Настройки по умолчанию для расширения autodoc, которое автоматически извлекает docstring'и
autodoc_default_options = {
    "members": True,
    "undoc-members": False,  # Не показывать недокументированные члены
    "private-members": False,  # Не показывать приватные методы (_method)
    "special-members": False,  # Не показывать __init__, __str__ и т.д.
    "inherited-members": False,  # Показывать унаследованные методы
    "show-inheritance": True,  # Показывать иерархию наследования
}

# Настройки для myst_parser
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
    "version_selector": True,
    "language_selector": False,  # отключено, если не нужно
    "flyout_display": "attached",  # или 'hidden' — по усмотрению
    # === Навигация ===
    "prev_next_buttons_location": "bottom",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    # === Визуальные настройки ===
    "style_nav_header_background": "#2980B9",  # цвет шапки
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
