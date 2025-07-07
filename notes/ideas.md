# TODO
1. Автоматизировать Dockerfile - чтобы в зависимости от содержимого requirements.txt скрипт определял,
какие зависимости нужны и добавлял их к python 3.11 slim

2. Улучшить diagram_auto_update - он должен автоматически определять корень текущего проекта

3. EditorConfig - настройки для текстовых редакторов. Пока необязательно, в будущем может быть полезно


# MUST HAVE
Полезная статья на будущее 

https://habr.com/ru/companies/otus/articles/713992/

1. Тестирование
- unittest
- pytest
- тесты на покрытие
2. CI 
- Github Actions
- GitlabCI
3. Pre-commit - проверка коммитов перед отправкой
4. Стиль кода и форматирование
- Black
- autopep8
- isort
5. Линтинг
- flake8
- pylint
- ruff
- Bandit (линтер безопасности)
6. Документация
- interrogate
- Sphinx
- autodoc
