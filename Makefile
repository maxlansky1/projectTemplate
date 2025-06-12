# Название Docker Compose файла (если нужно — можно менять)
COMPOSE_FILE=docker-compose.yaml
SERVICE ?= app

.PHONY: up down clean logs restart bash shell build

# 📦 Собрать и запустить контейнеры (в фоновом режиме)
up:
    docker-compose -f $(COMPOSE_FILE) up -d --build

# 🔨 Только сборка (без запуска)
build:
    docker-compose -f $(COMPOSE_FILE) build

# ⛔ Остановить все контейнеры
down:
    docker-compose -f $(COMPOSE_FILE) down

# 🧹 Полная остановка + удаление томов (данных)
clean:
    docker-compose -f $(COMPOSE_FILE) down -v

# 🔍 Просмотреть логи всех сервисов
logs:
    docker-compose -f $(COMPOSE_FILE) logs -f

# 🛠️ Перезапустить контейнеры (например, после изменений)
restart:
    docker-compose -f $(COMPOSE_FILE) down
    docker-compose -f $(COMPOSE_FILE) up -d --build

# 🖥️ Зайти внутрь контейнера (по умолчанию — сервис 'app')
bash:
    docker-compose -f $(COMPOSE_FILE) exec $(SERVICE) /bin/bash

# 🖥️ Альтернатива, если bash недоступен
shell:
    docker-compose -f $(COMPOSE_FILE) exec $(SERVICE) /bin/sh