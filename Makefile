# ================================
# 🛠️ Makefile
# ================================

# Считываем переменные окружения
include .env

# Указывает, какой файл docker-compose используется
COMPOSE_FILE=docker-compose.yaml

# Сервис по умолчанию (например, app)
SERVICE ?= app

# Список всех доступных задач
.PHONY: help up down restart build rebuild logs bash prune docs-clean docs-html

# =============================================
# 📌 ОСНОВНЫЕ КОМАНДЫ
# =============================================

# ▶️ Запуск контейнеров в фоне
# Используй после сборки или при старте проекта
up:
	docker-compose -f $(COMPOSE_FILE) up -d

# ⛔ Остановить все контейнеры проекта
# Не удаляет образы и данные
down:
	docker-compose -f $(COMPOSE_FILE) down

# 🔁 Перезапустить контейнеры без пересборки
# Полезно, если изменился код, но не зависимости
restart:
	$(MAKE) down
	$(MAKE) up

# 🔨 Пересобрать образы с нуля + очистка мусора
# Только для изменений в requirements.txt или Dockerfile
build:
	docker-compose -f $(COMPOSE_FILE) build --no-cache
	$(MAKE) prune

# 🔁🔄 Полный цикл: остановка → пересборка → запуск
# Используй, если хочешь всё обновить "от и до"
rebuild: down build up

# 🔍 Просмотр логов в реальном времени
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# 🖥️ Вход внутрь контейнера через bash (или sh)
bash:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE) /bin/bash || \
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE) /bin/sh

# 🗑️ Очистка: удаление остановленных контейнеров и старых образов этого проекта
prune:
	docker-compose -f $(COMPOSE_FILE) down --rmi local --volumes

# Очистка сгенерированной документации
docs-clean:
	.\docs\make.bat clean

# Сборка HTML-документации
docs-html:
	.\docs\make.bat html

# =============================================
# 💡 ПАМЯТКА: Какие команды когда использовать
# =============================================

# 🟢 При первом запуске или после изменений в окружении:
# make up

# 🟡 После изменений в коде (не в зависимостях):
# make restart

# 🔵 После изменений в requirements.txt или Dockerfile:
# make build

# 🔴 Чтобы всё пересобрать "с нуля" и полностью перезапустить:
# make rebuild

# 🟣 Чтобы посмотреть логи:
# make logs

# 🟠 Чтобы залезть внутрь контейнера:
# make bash

# ⚫ Чтобы освободить место на диске:
# make prune

# 🟤 Для справки:
help:
	@echo "📌 Доступные команды:"
	@echo ""
	@echo "  make up            ➜ Запустить контейнеры"
	@echo "  make down          ➜ Остановить контейнеры"
	@echo "  make restart       ➜ Перезапустить (без пересборки)"
	@echo "  make build         ➜ Пересобрать образы с нуля"
	@echo "  make rebuild       ➜ Полный цикл: down → build → up"
	@echo "  make logs          ➜ Посмотреть логи"
	@echo "  make bash          ➜ Войти в контейнер"
	@echo "  make prune         ➜ Почистить старые данные"
	@echo "  make help          ➜ Эта справка"
