# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Проверяем, какая операционная система
if os.name == "nt":  # Для Windows
    plantuml = r"java -jar C:\plantuml\plantuml.jar"
elif os.name == "posix":  # Для github workflows
    plantuml = "java -jar /home/runner/plantuml/plantuml.jar"
else:
    raise OSError("Unsupported OS")

# Настройка вывода изображений
plantuml_output_format = "svg"
plantuml_latex_output_format = "svg"

project = "projectTemplate"
copyright = "2025, gleb"
author = "gleb"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # автодока из docstring'ов
    "sphinx.ext.viewcode",  # ссылки на исходники
    "sphinx.ext.napoleon",  # Google/NumPy стиль docstring'ов
    "sphinx.ext.githubpages",  # позволяет использовать стили sphinx при хостинге доков на github pages
    "sphinx_autodoc_typehints",  # type hints в сигнатурах
    "myst_parser",  # поддержка Markdown (.md)
    "sphinx.ext.todo",  # поддержка TODO
    "sphinx.ext.coverage",  # проверяет покрытие документации
    "sphinx.ext.ifconfig",  # условные директивы в документации
    "sphinx_copybutton",  # добавляет кнопку скопировать код в документацию
    "sphinxcontrib.plantuml",  # добавляет поддержку plantuml
    "sphinx_rtd_theme",  # переключает на красивую тему
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,  # Не показывать недокументированные члены
    "private-members": False,  # Не показывать приватные методы (_method)
    "special-members": False,  # Не показывать __init__, __str__ и т.д.
    "inherited-members": False,  # Показывать унаследованные методы
    "show-inheritance": True,  # Показывать иерархию наследования
}

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "ru"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
