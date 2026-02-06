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
ENV API_URL=http://127.0.0.1:8000/predict
ENV PORT=8000

# Порт
EXPOSE 8000

# ПРАВИЛЬНЫЙ ЗАПУСК
CMD ["sh", "-c", "uvicorn cvd-risk-api.app.main:app --host 0.0.0.0 --port 8000 & sleep 10 && python bot/bot_main.py"]
