#!/bin/bash

echo "========================================"
echo "🤖 CVD Risk Telegram Bot"
echo "========================================"
echo ""

# Проверка .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo ""
    echo "📝 Создайте .env файл:"
    echo "1. cp .env.example .env"
    echo "2. nano .env (или любой редактор)"
    echo "3. Вставьте ваш TELEGRAM_BOT_TOKEN"
    echo ""
    exit 1
fi

echo "✅ Конфигурация найдена"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python не найден! Установите Python 3.11+"
    exit 1
fi

echo "✅ Python установлен"
echo ""

# Проверка зависимостей
echo "📦 Проверка зависимостей..."
if ! python3 -c "import telegram" &> /dev/null; then
    echo "⚠️ Зависимости не установлены"
    echo "📥 Устанавливаю зависимости..."
    pip3 install -r requirements_bot.txt
    if [ $? -ne 0 ]; then
        echo "❌ Ошибка установки зависимостей"
        exit 1
    fi
fi

echo "✅ Зависимости готовы"
echo ""

# Проверка API
echo "🔍 Проверка API..."
if ! curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "⚠️ API сервер не отвечает на http://localhost:8000"
    echo ""
    echo "🚀 СНАЧАЛА запустите API:"
    echo "   1. Откройте НОВЫЙ терминал"
    echo "   2. cd cvd-risk-api"
    echo "   3. uvicorn app.main:app --host 0.0.0.0 --port 8000"
    echo ""
    echo "После запуска API запустите этот скрипт снова"
    echo ""
    exit 1
fi

echo "✅ API работает"
echo ""

echo "🚀 Запускаю бота..."
echo "========================================"
echo ""

# Загрузка переменных из .env
export $(cat .env | grep -v '^#' | xargs)

python3 bot/bot_main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Ошибка запуска бота"
    echo "Проверьте логи выше"
fi
