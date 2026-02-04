@echo off
chcp 65001 > nul
echo ========================================
echo 🤖 CVD Risk Telegram Bot
echo ========================================
echo.

REM Проверка .env файла
if not exist .env (
    echo ❌ Файл .env не найден!
    echo.
    echo 📝 Создайте .env файл:
    echo 1. Скопируйте .env.example как .env
    echo 2. Откройте .env в блокноте
    echo 3. Вставьте ваш TELEGRAM_BOT_TOKEN
    echo.
    pause
    exit /b 1
)

echo ✅ Конфигурация найдена
echo.

REM Проверка Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.11+
    pause
    exit /b 1
)

echo ✅ Python установлен
echo.

REM Проверка зависимостей
echo 📦 Проверка зависимостей...
pip show python-telegram-bot > nul 2>&1
if errorlevel 1 (
    echo ⚠️ Зависимости не установлены
    echo 📥 Устанавливаю зависимости...
    pip install -r requirements_bot.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
)

echo ✅ Зависимости готовы
echo.

REM Проверка API
echo 🔍 Проверка API...
curl -s http://localhost:8000/ > nul 2>&1
if errorlevel 1 (
    echo ⚠️ API сервер не отвечает на http://localhost:8000
    echo.
    echo 🚀 СНАЧАЛА запустите API:
    echo    1. Откройте НОВЫЙ терминал
    echo    2. cd cvd-risk-api
    echo    3. uvicorn app.main:app --host 0.0.0.0 --port 8000
    echo.
    echo После запуска API запустите этот скрипт снова
    echo.
    pause
    exit /b 1
)

echo ✅ API работает
echo.

echo 🚀 Запускаю бота...
echo ========================================
echo.

python bot/bot_main.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска бота
    echo Проверьте логи выше
    pause
)
