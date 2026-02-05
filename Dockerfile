FROM python:3.11-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements_bot.txt .
COPY cvd-risk-api/requirements.txt requirements_api.txt

# Устанавливаем Python пакеты
RUN pip install --no-cache-dir -r requirements_bot.txt
RUN pip install --no-cache-dir -r requirements_api.txt

# Копируем весь проект
COPY . .

# Переменные окружения
ENV PYTHONPATH=/app
ENV PORT=8000

# Порт
EXPOSE 8000

# ИСПРАВЛЕННЫЙ ЗАПУСК: API в фоне, затем бот на переднем плане
CMD ["sh", "-c", "export PYTHONPATH=$PYTHONPATH:/app/cvd-risk-api && uvicorn app.main:app --app-dir cvd-risk-api --host 0.0.0.0 --port ${PORT:-8000} & sleep 5 && python bot/bot_main.py"]

