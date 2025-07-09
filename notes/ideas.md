# TODO
1. Автоматизировать Dockerfile - чтобы в зависимости от содержимого requirements.txt скрипт определял,
какие зависимости нужны и добавлял их к python 3.11 slim

2. Улучшить diagram_auto_update - он должен автоматически определять корень текущего проекта

3. EditorConfig - настройки для текстовых редакторов. Пока необязательно, в будущем может быть полезно

4. Улучшить pre-commit
- доделать CI/CD
- доделать линтеры Make, Docker, GitHub
    - Hadolint (docker)

5. Доделать Sphinx
- внедрить plantuml?
- сделать красивое оформление Make и Docker в документации
- посмотреть примеры топ компаний

6. Сделать тесты и покрытие 


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
- Стиль кода и форматирование
black
- Линтинг
- ruff
- Bandit (линтер безопасности)

4. Документация
- Sphinx
- autodoc
