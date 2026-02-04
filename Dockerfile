FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements_bot.txt .
COPY cvd-risk-api/requirements.txt requirements_api.txt

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements_bot.txt
RUN pip install --no-cache-dir -r requirements_api.txt

# Копирование всего проекта
COPY . .

# Переменные окружения (будут переопределены в Render)
ENV TELEGRAM_BOT_TOKEN=""
ENV API_URL="http://localhost:8000/predict"
ENV DAILY_LIMIT=10
ENV RATE_LIMIT_MINUTES=1

# Expose порт для API
EXPOSE 8000

# Скрипт запуска (запускает API и бота одновременно)
CMD ["sh", "-c", "uvicorn cvd-risk-api.app.main:app --host 0.0.0.0 --port 8000 & python bot/bot_main.py"]