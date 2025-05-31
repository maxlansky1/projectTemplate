# ✅ Базовый минимальный образ Python 3.11 на Debian без лишних пакетов
FROM python:3.11-slim

# ✅ Установка рабочей директории внутри контейнера
WORKDIR /app

# ✅ Устанавливаем системные зависимости, необходимые для сборки C-библиотек (например, lxml, opencv, numpy)
# --no-install-recommends не тащит лишние пакеты

# ПРИМЕЧАНИЕ: По умолчанию отключено, нужно каждый раз уточнять исходя из зависимостей проекта

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \            # gcc, g++, make — нужны для сборки C-зависимостей
#     libglib2.0-0 \               # для OpenCV
#     libgl1 \                     # для OpenCV
#     libxml2-dev libxslt1-dev \  # для lxml
#     libjpeg-dev zlib1g-dev \    # для Pillow (работа с изображениями)
#     curl \                       # часто нужен для отладки/проверки сетей
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# ✅ Копируем только requirements.txt, чтобы использовать кэш Docker при установке зависимостей
COPY requirements.txt .

# ✅ Установка зависимостей проекта
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Копируем оставшиеся файлы проекта внутрь контейнера
COPY . .

# ✅ Переменные окружения - отключает буферизацию stdout/stderr, чтобы логи сразу появлялись. задает локальное время
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# ✅ (Опционально) делаем основной файл исполняемым
RUN chmod +x ./src/main.py

# ✅ Команда по умолчанию для запуска приложения
CMD ["python", "src/main.py"]
