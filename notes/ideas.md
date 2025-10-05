## 🐳 Docker
- [ ] Доделать линтеры Make, Docker, GitHub
- [ ] Hadolint (docker)
- [x] Проблемы с кодировкой логов при `docker logs`

## 📦 CI/CD и Автоматизация
- [ ] Управление шаблоном через copier
- [x] Доделать CI/CD
- [x] Улучшить `pre-commit`
- [x] Улучшить `deploy_app`
  - [x] на данный момент есть проблемы, т.к `ssh-action` не отдает переменные в ENV → не получается отправить в телеграм выводы команд из консоли 
  - [x] дважды пересобирает при `make rebuild`
  - [x] улучшить фильтр на событие push - не всегда нужно пересобирать контейнер
- [ ] Переписать deploy_app и deploy_docs под новые правила гитхаб (https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/)

## 📄 Документация и диаграммы
- [ ] Доделать Sphinx
  - [x] внедрить plantuml?
  - [ ] сделать красивое оформление Make и Docker в документации
  - [ ] добавить поддержку вкладок в документацию? https://github.com/executablebooks/sphinx-tabs
  - [ ] добавить кастомный дизайн? https://sphinx-design.readthedocs.io/
- [x] Настроить деплой на GitHub Pages
  - [x] отредактировать размер диаграммы
- [ ] Добавить CHANGELOG.md (https://keepachangelog.com/en/1.1.0/)

## 🧪 Тестирование
- [ ] Сделать тесты и покрытие (unittest, pytest)

## 🛠 Инструменты и настройки
- [ ] EditorConfig — настройки для текстовых редакторов. Пока необязательно, в будущем может быть полезно
- [ ] Управление зависимостями - uv? pip? poetry? pyproject.toml
- [ ] Логирование - пересобрать логгер
 
## 📝 TODO
- [ ] Сделать нормальный TODO
- [ ] Сделать трекер задач



# Полезные ссылки
Полезная статья на будущее 
https://habr.com/ru/companies/otus/articles/713992/


5. Визуализация репозитория (прикрутить к репо?)
https://githubnext.com/projects/repo-visualization


Шаблоны проектирования
https://python-patterns.guide/

Сравнение библиотек
https://www.libhunt.com/

Пример управления проектом
https://blog.dusktreader.dev/2025/04/06/bootstrapping-python-projects-with-copier/#to-github

OpenGraph - настройка сайта для шеринга в соцсетях
https://habr.com/ru/companies/click/articles/492258/