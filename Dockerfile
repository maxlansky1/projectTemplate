# Начинаем сборку с образа Python slim, чтобы сократить размер приложения
FROM python:3.12-slim

# Импортируем нужные переменные (импортируются по пути .env -> docker-compose -> Dockerfile)
ARG DEPLOY_USER_NAME
ARG UID
ARG GID
ARG APP_NAME
ARG APP_PORT

# Устанавливаем локали (без вывода предупреждений)
RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения для локалей
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Устанавливаем PYTHONPATH и PATH
ENV PYTHONPATH /${APP_NAME}
ENV PATH /home/${DEPLOY_USER_NAME}/.local/bin:$PATH

# Устанавливаем рабочую директорию
WORKDIR /${APP_NAME}

# Создаём пользователя ДО установки зависимостей и даем ему права на чтение и запись
RUN groupadd -g ${GID} ${DEPLOY_USER_NAME} && \
    useradd -m -u ${UID} -g ${DEPLOY_USER_NAME} ${DEPLOY_USER_NAME}

# Копируем requirements
COPY requirements.txt .

# Устанавливаем зависимости от root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код в контейнер с правами нового юзера
COPY --chown=${DEPLOY_USER_NAME}:${DEPLOY_USER_NAME} . .

# Переключаемся на нового юзера
USER ${DEPLOY_USER_NAME}

# Проверяем состояния контейнера
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:${APP_PORT}/health || exit 1

# Запуск приложения
CMD ["python", "-m", "src.main"]