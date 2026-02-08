"""
CVD Risk Prediction Telegram Bot
Минимальная версия с полным функционалом
"""

import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import requests

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# ==========================================
# КОНФИГУРАЦИЯ
# ==========================================

# Telegram Bot Token (получите у @BotFather)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# API эндпоинт (локальный или удаленный)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

# Лимиты использования
DAILY_LIMIT = int(os.getenv("DAILY_LIMIT", "10"))  # запросов в день на пользователя
RATE_LIMIT_MINUTES = int(os.getenv("RATE_LIMIT_MINUTES", "1"))  # минимум между запросами

# Файл для хранения данных пользователей (лимиты)
USER_DATA_FILE = "bot_users.json"

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# СОСТОЯНИЯ РАЗГОВОРА
# ==========================================

(LANGUAGE, AGE, GENDER, AP_HI, AP_LO, 
 CHOLESTEROL, GLUCOSE, HEIGHT, WEIGHT,  
 SMOKE, ALCOHOL, ACTIVITY) = range(12)

# ==========================================
# МНОГОЯЗЫЧНЫЕ ТЕКСТЫ
# ==========================================

MESSAGES = {
    "ru": {
        "start": "👋 Добро пожаловать в бот прогнозирования сердечно-сосудистого риска!\n\n"
                 "Этот бот использует ML-модель для оценки вашего риска развития CVD.\n\n"
                 "⚠️ ВАЖНО: Это не медицинская консультация! Результаты должны интерпретироваться врачом.\n\n"
                 "📊 У вас есть {remaining} из {total} анализов сегодня.\n\n"
                 "Выберите язык:",
        "help": "📖 Доступные команды:\n\n"
                "/start - Начать новый анализ\n"
                "/help - Показать эту справку\n"
                "/stats - Ваша статистика\n"
                "/cancel - Отменить текущий анализ\n\n"
                "❓ Как это работает:\n"
                "1. Бот попросит ввести ваши данные\n"
                "2. ML-модель проанализирует риск\n"
                "3. Вы получите детальный отчет\n\n"
                "⚠️ Результаты не заменяют консультацию врача!",
        "stats": "📊 Ваша статистика:\n\n"
                 "Использовано сегодня: {used}/{total}\n"
                 "Осталось анализов: {remaining}\n"
                 "Всего выполнено: {total_predictions}\n"
                 "Последний анализ: {last_prediction}",
        "limit_reached": "⚠️ Вы достигли дневного лимита ({limit} анализов).\n"
                        "Попробуйте завтра!",
        "rate_limited": "⏱ Пожалуйста, подождите {seconds} секунд между запросами.",
        "canceled": "❌ Анализ отменен. Используйте /start для нового анализа.",
        
        # Вопросы
        "ask_age": "Введите ваш возраст (лет):",
        "ask_gender": "Выберите пол:",
        "ask_ap_hi": "Введите систолическое давление (верхнее, мм рт.ст.):\nНапример: 120",
        "ask_ap_lo": "Введите диастолическое давление (нижнее, мм рт.ст.):\nНапример: 80",
        "ask_cholesterol": (
            "📊 Уровень холестерина:\n\n"
            "🟢 Норма — анализы в норме ИЛИ вы ведете здоровый образ жизни и нет лишнего веса.\n"
            "🟡 Выше нормы — врач ранее отмечал повышение ИЛИ вы часто употребляете жирную пищу.\n"
            "🔴 Высокий — диагностирована гиперлипидемия ИЛИ были ранние инфаркты у родных."
        ),
        "ask_glucose": (
            "🍭 Уровень глюкозы:\n\n"
            "🟢 Норма — сахар всегда в норме ИЛИ у вас нет лишнего веса и тяги к сладкому.\n"
            "🟡 Выше нормы — был замечен «пограничный» сахар ИЛИ вы мало двигаетесь.\n"
            "🔴 Высокий — диагностирован диабет ИЛИ вы принимаете сахароснижающие препараты."
        ),
        "ask_height": "Введите ваш рост (см):\nНапример: 170",
        "ask_weight": "Введите ваш вес (кг):\nНапример: 75",
        "ask_smoke": "Вы курите?",
        "ask_alcohol": "Употребляете алкоголь?",
        "ask_activity": "Занимаетесь физической активностью?",
        
        # Варианты ответов
        "male": "👨 Мужской",
        "female": "👩 Женский",
        "normal": "✅ Норма",
        "above_normal": "⚠️ Выше нормы",
        "high": "🔴 Высокий",
        "yes": "✅ Да",
        "no": "❌ Нет",
        
        # Обработка
        "processing": "🔄 Анализирую ваши данные...",
        "error": "❌ Произошла ошибка. Попробуйте снова /start",
        "invalid_input": "⚠️ Пожалуйста, введите корректное значение.",
        
        # Результат
        "result_header": "📊 РЕЗУЛЬТАТЫ АНАЛИЗА\n" + "=" * 30 + "\n",
        "risk_probability": "🎯 Вероятность риска: {prob}%",
        "risk_category": "📈 Категория: {category}",
        "confidence": "🔍 Достоверность: {level}\n{note}",
        "factors_header": "\n💡 ФАКТОРЫ РИСКА:",
        "factor_item": "• {factor}: {note}",
        "conditions_header": "\n⚕️ КЛИНИЧЕСКИЕ СОСТОЯНИЯ:",
        "condition_item": "• {condition} ({severity})\n  {note}",
        "warnings_header": "\n⚠️ ПРЕДУПРЕЖДЕНИЯ:",
        "warning_item": "• {warning}",
        "disclaimer": "\n\n⚠️ ВАЖНО:\n{text}",
        "metrics_info": "\n📊 Точность модели:\n"
                       "Sensitivity: {sensitivity}%\n"
                       "Specificity: {specificity}%\n"
                       "ROC-AUC: {roc_auc}",
        # Кнопки быстрых действий
        "btn_new_analysis": "🔄 Новый анализ",
        "btn_stats": "📊 Моя статистика",  
        "btn_help": "❓ Помощь",
        "after_result": "Что хотите сделать дальше?",
        
    },
    
    "en": {
        "start": "👋 Welcome to the Cardiovascular Risk Prediction Bot!\n\n"
                 "This bot uses an ML model to assess your CVD risk.\n\n"
                 "⚠️ IMPORTANT: This is NOT medical advice! Results should be interpreted by a doctor.\n\n"
                 "📊 You have {remaining} of {total} analyses today.\n\n"
                 "Choose your language:",
        "help": "📖 Available commands:\n\n"
                "/start - Start new analysis\n"
                "/help - Show this help\n"
                "/stats - Your statistics\n"
                "/cancel - Cancel current analysis\n\n"
                "❓ How it works:\n"
                "1. Bot will ask for your data\n"
                "2. ML model analyzes the risk\n"
                "3. You get a detailed report\n\n"
                "⚠️ Results don't replace doctor consultation!",
        "stats": "📊 Your statistics:\n\n"
                 "Used today: {used}/{total}\n"
                 "Remaining: {remaining}\n"
                 "Total predictions: {total_predictions}\n"
                 "Last prediction: {last_prediction}",
        "limit_reached": "⚠️ You've reached the daily limit ({limit} analyses).\n"
                        "Try again tomorrow!",
        "rate_limited": "⏱ Please wait {seconds} seconds between requests.",
        "canceled": "❌ Analysis canceled. Use /start for a new analysis.",
        
        "ask_age": "Enter your age (years):",
        "ask_gender": "Choose your gender:",
        "ask_ap_hi": "Enter systolic blood pressure (upper, mmHg):\nExample: 120",
        "ask_ap_lo": "Enter diastolic blood pressure (lower, mmHg):\nExample: 80",
        "ask_cholesterol": (
            "📊 Cholesterol level:\n\n"
            "🟢 Normal — results are normal OR you lead a healthy lifestyle and have no excess weight.\n"
            "🟡 Above Normal — doctor noted a slight increase OR you frequently eat fatty/fried foods.\n"
            "🔴 High — diagnosed hyperlipidemia OR family history of early heart attacks."
        ),
        "ask_glucose": (
            "🍭 Glucose level:\n\n"
            "🟢 Normal — glucose is always normal OR you have no excess weight and no sweet cravings.\n"
            "🟡 Above Normal — doctor noted a borderline glucose level OR you are not very active.\n"
            "🔴 High — diagnosed diabetes OR you are taking glucose-lowering medications."
        ),
        "ask_height": "Enter your height (cm):\nExample: 170",
        "ask_weight": "Enter your weight (kg):\nExample: 75",
        "ask_smoke": "Do you smoke?",
        "ask_alcohol": "Do you consume alcohol?",
        "ask_activity": "Do you exercise regularly?",
        
        "male": "👨 Male",
        "female": "👩 Female",
        "normal": "✅ Normal",
        "above_normal": "⚠️ Above Normal",
        "high": "🔴 High",
        "yes": "✅ Yes",
        "no": "❌ No",
        
        "processing": "🔄 Analyzing your data...",
        "error": "❌ An error occurred. Try again /start",
        "invalid_input": "⚠️ Please enter a valid value.",
        
        "result_header": "📊 ANALYSIS RESULTS\n" + "=" * 30 + "\n",
        "risk_probability": "🎯 Risk probability: {prob}%",
        "risk_category": "📈 Category: {category}",
        "confidence": "🔍 Confidence: {level}\n{note}",
        "factors_header": "\n💡 RISK FACTORS:",
        "factor_item": "• {factor}: {note}",
        "conditions_header": "\n⚕️ CLINICAL CONDITIONS:",
        "condition_item": "• {condition} ({severity})\n  {note}",
        "warnings_header": "\n⚠️ WARNINGS:",
        "warning_item": "• {warning}",
        "disclaimer": "\n\n⚠️ IMPORTANT:\n{text}",
        "metrics_info": "\n📊 Model accuracy:\n"
                       "Sensitivity: {sensitivity}%\n"
                       "Specificity: {specificity}%\n"
                       "ROC-AUC: {roc_auc}",
        
        "btn_new_analysis": "🔄 New Analysis",
        "btn_stats": "📊 My Statistics",
        "btn_help": "❓ Help",
        "after_result": "What would you like to do next?",        
    },
    
    "kr": {
        "start": "👋 심혈관 위험 예측 봇에 오신 것을 환영합니다!\n\n"
                 "이 봇은 ML 모델을 사용하여 CVD 위험을 평가합니다.\n\n"
                 "⚠️ 중요: 의학적 조언이 아닙니다! 결과는 의사가 해석해야 합니다.\n\n"
                 "📊 오늘 {remaining}/{total}개의 분석이 남았습니다.\n\n"
                 "언어를 선택하세요:",
        "help": "📖 사용 가능한 명령어:\n\n"
                "/start - 새 분석 시작\n"
                "/help - 도움말 표시\n"
                "/stats - 통계\n"
                "/cancel - 현재 분석 취소\n\n"
                "❓ 작동 방식:\n"
                "1. 봇이 데이터를 요청합니다\n"
                "2. ML 모델이 위험을 분석합니다\n"
                "3. 상세한 보고서를 받습니다\n\n"
                "⚠️ 결과가 의사 상담을 대체하지 않습니다!",
        "stats": "📊 통계:\n\n"
                 "오늘 사용: {used}/{total}\n"
                 "남은 분석: {remaining}\n"
                 "총 예측: {total_predictions}\n"
                 "마지막 예측: {last_prediction}",
        "limit_reached": "⚠️ 일일 한도에 도달했습니다 ({limit}개 분석).\n"
                        "내일 다시 시도하세요!",
        "rate_limited": "⏱ 요청 사이에 {seconds}초를 기다려 주세요.",
        "canceled": "❌ 분석이 취소되었습니다. 새 분석을 위해 /start를 사용하세요.",
        
        "ask_age": "나이를 입력하세요 (년):",
        "ask_gender": "성별을 선택하세요:",
        "ask_ap_hi": "수축기 혈압을 입력하세요 (상단, mmHg):\n예: 120",
        "ask_ap_lo": "이완기 혈압을 입력하세요 (하단, mmHg):\n예: 80",
        "ask_cholesterol": (
            "📊 콜레스테롤 수준:\n\n"
            "🟢 정상 — 검사 결과가 정상이거나 건강한 생활 방식을 유지하고 있으며 과체중이 아닙니다.\n"
            "🟡 정상 초과 — 의료진이 약간 높은 수치를 기록했거나 자주 지방이 많은 음식을 섭취합니다.\n"
            "🔴 높음 — 고지혈증 진단 또는 가족력이 있는 경우."
        ),
        "ask_glucose": (
            "🍭 포도당 수준:\n\n"
            "🟢 정상 — 포도당 수치가 항상 정상이거나 과체중이 없고 당분 섭취에 대한 욕구가 없습니다.\n"
            "🟡 정상 초과 — 의료진이 경계선 수치를 기록했거나 활동성이 낮습니다.\n"
            "🔴 높음 — 당뇨병 진단 또는 혈당 강하제 복용 중입니다."
        ),
        "ask_height": "키를 입력하세요 (cm):\n예: 170",
        "ask_weight": "체중을 입력하세요 (kg):\n예: 75",
        "ask_smoke": "흡연하십니까?",
        "ask_alcohol": "음주하십니까?",
        "ask_activity": "규칙적으로 운동하십니까?",
        
        "male": "👨 남성",
        "female": "👩 여성",
        "normal": "✅ 정상",
        "above_normal": "⚠️ 정상 이상",
        "high": "🔴 높음",
        "yes": "✅ 예",
        "no": "❌ 아니오",
        
        "processing": "🔄 데이터를 분석 중입니다...",
        "error": "❌ 오류가 발생했습니다. /start를 다시 시도하세요",
        "invalid_input": "⚠️ 올바른 값을 입력하세요.",
        
        "result_header": "📊 분석 결과\n" + "=" * 30 + "\n",
        "risk_probability": "🎯 위험 확률: {prob}%",
        "risk_category": "📈 범주: {category}",
        "confidence": "🔍 신뢰도: {level}\n{note}",
        "factors_header": "\n💡 위험 요인:",
        "factor_item": "• {factor}: {note}",
        "conditions_header": "\n⚕️ 임상 상태:",
        "condition_item": "• {condition} ({severity})\n  {note}",
        "warnings_header": "\n⚠️ 경고:",
        "warning_item": "• {warning}",
        "disclaimer": "\n\n⚠️ 중요:\n{text}",
        "metrics_info": "\n📊 모델 정확도:\n"
                       "민감도: {sensitivity}%\n"
                       "특이도: {specificity}%\n"
                       "ROC-AUC: {roc_auc}",
        "btn_new_analysis": "🔄 새 분석",
        "btn_stats": "📊 내 통계",
        "btn_help": "❓ 도움말",
        "after_result": "다음에 무엇을 하시겠습니까?",        
    }
}

# ==========================================
# УПРАВЛЕНИЕ ДАННЫМИ ПОЛЬЗОВАТЕЛЕЙ
# ==========================================

def load_user_data() -> Dict:
    """Загрузка данных пользователей из файла"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data: Dict):
    """Сохранение данных пользователей в файл"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def check_rate_limit(user_id: int) -> tuple[bool, int]:
    """
    Проверка лимитов пользователя
    Возвращает (can_proceed, seconds_to_wait)
    """
    user_data = load_user_data()
    user_id_str = str(user_id)
    
    now = datetime.now()
    today = now.date().isoformat()
    
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "total_predictions": 0,
            "daily_usage": {},
            "last_request": None
        }
    
    user = user_data[user_id_str]
    
    # Проверка дневного лимита
    if today not in user["daily_usage"]:
        user["daily_usage"] = {today: 0}  # Сброс для нового дня
    
    if user["daily_usage"][today] >= DAILY_LIMIT:
        return False, -1  # Дневной лимит достигнут
    
    # Проверка rate limit (минуты между запросами)
    if user["last_request"]:
        last_request = datetime.fromisoformat(user["last_request"])
        time_passed = (now - last_request).total_seconds()
        min_interval = RATE_LIMIT_MINUTES * 60
        
        if time_passed < min_interval:
            return False, int(min_interval - time_passed)
    
    return True, 0

def increment_user_usage(user_id: int):
    """Увеличение счетчика использования"""
    user_data = load_user_data()
    user_id_str = str(user_id)
    today = datetime.now().date().isoformat()
    
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "total_predictions": 0,
            "daily_usage": {},
            "last_request": None
        }
    
    user = user_data[user_id_str]
    
    if today not in user["daily_usage"]:
        user["daily_usage"] = {today: 0}
    
    user["daily_usage"][today] += 1
    user["total_predictions"] += 1
    user["last_request"] = datetime.now().isoformat()
    
    save_user_data(user_data)

def get_user_stats(user_id: int) -> Dict:
    """Получение статистики пользователя"""
    user_data = load_user_data()
    user_id_str = str(user_id)
    today = datetime.now().date().isoformat()
    
    if user_id_str not in user_data:
        return {
            "used": 0,
            "remaining": DAILY_LIMIT,
            "total_predictions": 0,
            "last_prediction": "Никогда"
        }
    
    user = user_data[user_id_str]
    used = user["daily_usage"].get(today, 0)
    
    last_pred = "Никогда"
    if user["last_request"]:
        last_pred = datetime.fromisoformat(user["last_request"]).strftime("%Y-%m-%d %H:%M")
    
    return {
        "used": used,
        "remaining": DAILY_LIMIT - used,
        "total_predictions": user["total_predictions"],
        "last_prediction": last_pred
    }

# ==========================================
# КОМАНДЫ БОТА
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Команда /start - начало разговора"""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    
    # Проверка лимитов
    can_proceed, wait_seconds = check_rate_limit(user_id)
    
    if not can_proceed and wait_seconds == -1:
        lang = context.user_data.get('language', 'ru')
        await update.message.reply_text(
            MESSAGES[lang]["limit_reached"].format(limit=DAILY_LIMIT)
        )
        return ConversationHandler.END
    
    if not can_proceed and wait_seconds > 0:
        lang = context.user_data.get('language', 'ru')
        await update.message.reply_text(
            MESSAGES[lang]["rate_limited"].format(seconds=wait_seconds)
        )
        return ConversationHandler.END
    
    # Выбор языка
    keyboard = [
        ["🇷🇺 Русский", "🇬🇧 English", "🇰🇷 한국어"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES["ru"]["start"].format(
            remaining=stats["remaining"],
            total=DAILY_LIMIT
        ),
        reply_markup=reply_markup
    )
    
    return LANGUAGE

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    lang = context.user_data.get('language', 'ru')
    await update.message.reply_text(MESSAGES[lang]["help"])

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats - статистика пользователя"""
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)
    lang = context.user_data.get('language', 'ru')
    
    await update.message.reply_text(
        MESSAGES[lang]["stats"].format(**stats, total=DAILY_LIMIT)
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Команда /cancel - отмена разговора"""
    lang = context.user_data.get('language', 'ru')
    await update.message.reply_text(
        MESSAGES[lang]["canceled"],
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# ==========================================
# ОБРАБОТЧИКИ ВВОДА ДАННЫХ
# ==========================================

async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выбор языка"""
    text = update.message.text
    
    if "Русский" in text:
        context.user_data['language'] = 'ru'
    elif "English" in text:
        context.user_data['language'] = 'en'
    elif "한국어" in text:
        context.user_data['language'] = 'kr'
    else:
        context.user_data['language'] = 'ru'
    
    lang = context.user_data['language']
    context.user_data['patient_data'] = {'ui_language': lang}
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_age"],
        reply_markup=ReplyKeyboardRemove()
    )
    return AGE

async def age_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод возраста"""
    lang = context.user_data['language']
    
    try:
        age = int(update.message.text)
        if 18 <= age <= 90:
            context.user_data['patient_data']['age_years'] = age
            
            # Спрашиваем пол
            keyboard = [[MESSAGES[lang]["male"], MESSAGES[lang]["female"]]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await update.message.reply_text(
                MESSAGES[lang]["ask_gender"],
                reply_markup=reply_markup
            )
            return GENDER
        else:
            await update.message.reply_text(MESSAGES[lang]["invalid_input"])
            return AGE
    except ValueError:
        await update.message.reply_text(MESSAGES[lang]["invalid_input"])
        return AGE

async def gender_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод пола"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1 = female, 2 = male
    if MESSAGES[lang]["female"] in text:
        context.user_data['patient_data']['gender'] = 1
    else:
        context.user_data['patient_data']['gender'] = 2
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_ap_hi"],
        reply_markup=ReplyKeyboardRemove()
    )
    return AP_HI

async def ap_hi_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод систолического давления"""
    lang = context.user_data['language']
    
    try:
        ap_hi = int(update.message.text)
        if 90 <= ap_hi <= 220:
            context.user_data['patient_data']['ap_hi'] = ap_hi
            await update.message.reply_text(MESSAGES[lang]["ask_ap_lo"])
            return AP_LO
        else:
            await update.message.reply_text(MESSAGES[lang]["invalid_input"])
            return AP_HI
    except ValueError:
        await update.message.reply_text(MESSAGES[lang]["invalid_input"])
        return AP_HI

async def ap_lo_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод диастолического давления"""
    lang = context.user_data['language']
    
    try:
        ap_lo = int(update.message.text)
        if 50 <= ap_lo <= 140:
            context.user_data['patient_data']['ap_lo'] = ap_lo
            
            # Спрашиваем холестерин
            keyboard = [[
                MESSAGES[lang]["normal"],
                MESSAGES[lang]["above_normal"],
                MESSAGES[lang]["high"]
            ]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await update.message.reply_text(
                MESSAGES[lang]["ask_cholesterol"],
                reply_markup=reply_markup
            )
            return CHOLESTEROL
        else:
            await update.message.reply_text(MESSAGES[lang]["invalid_input"])
            return AP_LO
    except ValueError:
        await update.message.reply_text(MESSAGES[lang]["invalid_input"])
        return AP_LO

async def cholesterol_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод холестерина"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1=normal, 2=above normal, 3=high
    if MESSAGES[lang]["normal"] in text:
        cholesterol = 1
    elif MESSAGES[lang]["above_normal"] in text:
        cholesterol = 2
    else:
        cholesterol = 3
    
    context.user_data['patient_data']['cholesterol'] = cholesterol
    
    # Спрашиваем глюкозу
    keyboard = [[
        MESSAGES[lang]["normal"],
        MESSAGES[lang]["above_normal"],
        MESSAGES[lang]["high"]
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_glucose"],
        reply_markup=reply_markup
    )
    return GLUCOSE

async def glucose_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод глюкозы"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1=normal, 2=above normal, 3=high
    if MESSAGES[lang]["normal"] in text:
        glucose = 1
    elif MESSAGES[lang]["above_normal"] in text:
        glucose = 2
    else:
        glucose = 3
    
    context.user_data['patient_data']['gluc'] = glucose
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_height"],
        reply_markup=ReplyKeyboardRemove()
    )
    return HEIGHT

async def height_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод роста"""
    lang = context.user_data['language']
    
    try:
        height = float(update.message.text.replace(',', '.'))
        if 100 <= height <= 250:  # Рост от 100 до 250 см
            context.user_data['patient_data']['height'] = height
            
            await update.message.reply_text(
                MESSAGES[lang]["ask_weight"],
                reply_markup=ReplyKeyboardRemove()
            )
            return WEIGHT
        else:
            await update.message.reply_text(MESSAGES[lang]["invalid_input"])
            return HEIGHT
    except ValueError:
        await update.message.reply_text(MESSAGES[lang]["invalid_input"])
        return HEIGHT


async def weight_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод веса и автоматический расчет ИМТ"""
    lang = context.user_data['language']
    
    try:
        weight = float(update.message.text.replace(',', '.'))
        if 30 <= weight <= 300:  # Вес от 30 до 300 кг
            context.user_data['patient_data']['weight'] = weight
            
            # АВТОМАТИЧЕСКИЙ РАСЧЕТ ИМТ
            height_m = context.user_data['patient_data']['height'] / 100  # см в метры
            bmi = weight / (height_m ** 2)
            context.user_data['patient_data']['bmi'] = round(bmi, 1)
            
            # Показываем рассчитанный ИМТ пользователю
            bmi_message = {
                'ru': f"✅ Ваш ИМТ: {bmi:.1f} кг/м²",
                'en': f"✅ Your BMI: {bmi:.1f} kg/m²",
                'kr': f"✅ BMI: {bmi:.1f} kg/m²"
            }
            await update.message.reply_text(bmi_message.get(lang, bmi_message['en']))
            
            # Спрашиваем про курение
            keyboard = [[MESSAGES[lang]["yes"], MESSAGES[lang]["no"]]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            
            await update.message.reply_text(
                MESSAGES[lang]["ask_smoke"],
                reply_markup=reply_markup
            )
            return SMOKE
        else:
            await update.message.reply_text(MESSAGES[lang]["invalid_input"])
            return WEIGHT
    except ValueError:
        await update.message.reply_text(MESSAGES[lang]["invalid_input"])
        return WEIGHT

async def smoke_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод курения"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1=yes, 0=no
    if MESSAGES[lang]["yes"] in text:
        context.user_data['patient_data']['smoke'] = 1
    else:
        context.user_data['patient_data']['smoke'] = 0
    
    # Спрашиваем про алкоголь
    keyboard = [[MESSAGES[lang]["yes"], MESSAGES[lang]["no"]]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_alcohol"],
        reply_markup=reply_markup
    )
    return ALCOHOL

async def alcohol_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод алкоголя"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1=yes, 0=no
    if MESSAGES[lang]["yes"] in text:
        context.user_data['patient_data']['alco'] = 1
    else:
        context.user_data['patient_data']['alco'] = 0
    
    # Спрашиваем про активность
    keyboard = [[MESSAGES[lang]["yes"], MESSAGES[lang]["no"]]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        MESSAGES[lang]["ask_activity"],
        reply_markup=reply_markup
    )
    return ACTIVITY

async def activity_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ввод активности и отправка на анализ"""
    lang = context.user_data['language']
    text = update.message.text
    
    # 1=yes, 0=no
    if MESSAGES[lang]["yes"] in text:
        context.user_data['patient_data']['active'] = 1
    else:
        context.user_data['patient_data']['active'] = 0
    
    # Все данные собраны, отправляем на анализ
    await update.message.reply_text(
        MESSAGES[lang]["processing"],
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Вызываем API
    await send_prediction_request(update, context)
    
    return ConversationHandler.END

# ==========================================
# ОТПРАВКА ЗАПРОСА К API
# ==========================================

async def send_prediction_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка данных к API и обработка результата"""
    lang = context.user_data['language']
    
    # Создаем копию, чтобы не испортить исходные данные пользователя
    patient_data_for_api = context.user_data['patient_data'].copy()
    
    # УДАЛЯЕМ рост и вес, так как модель их не поддерживает
    patient_data_for_api.pop('height', None)
    patient_data_for_api.pop('weight', None)
    
    user_id = update.effective_user.id
    
    try:
        # Отправляем очищенные данные (patient_data_for_api)
        response = requests.post(
            API_URL,
            json=patient_data_for_api, # <--- Передаем очищенный словарь
            timeout=100 # Увеличили тайм-аут для тяжелых расчетов
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Увеличиваем счетчик использования
            increment_user_usage(user_id)
            
            # Форматируем результат
            message = format_prediction_result(result, lang)
            
            # Отправляем результат (разбиваем на части если слишком длинный)
            if len(message) > 4096:
                parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
                for i, part in enumerate(parts):
                    if i == len(parts) - 1:  # Последняя часть - с кнопками
                        await send_result_with_buttons(update, part, lang)
                    else:
                        await update.message.reply_text(part)
            else:
                await send_result_with_buttons(update, message, lang)
        else:
            await update.message.reply_text(
                f"{MESSAGES[lang]['error']}\n"
                f"API Error: {response.status_code}"
            )
    
    except requests.exceptions.ConnectionError:
        await update.message.reply_text(
            f"{MESSAGES[lang]['error']}\n"
            "❌ Не удается подключиться к API. Убедитесь, что сервер запущен."
        )
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        await update.message.reply_text(
            f"{MESSAGES[lang]['error']}\n"
            f"Details: {str(e)}"
        )

def format_prediction_result(result: Dict, lang: str) -> str:
    """Форматирование результата предсказания"""
    msg = MESSAGES[lang]
    
    # Заголовок
    text = msg["result_header"]
    
    # Основная информация
    risk_prob = result.get("risk_probability", 0) * 100
    text += msg["risk_probability"].format(prob=f"{risk_prob:.1f}") + "\n"
    text += msg["risk_category"].format(category=result.get("risk_label", "N/A")) + "\n\n"
    
    # Достоверность
    text += msg["confidence"].format(
        level=result.get("confidence_title", "N/A"),
        note=result.get("confidence_note", "")
    ) + "\n"
    
    # Факторы риска
    if result.get("clinical_explanation"):
        text += msg["factors_header"] + "\n"
        for factor in result["clinical_explanation"][:5]:  # Топ-5 факторов
            text += msg["factor_item"].format(
                factor=factor.get("factor", "N/A"),
                note=factor.get("clinical_note", "")
            ) + "\n"
    
    # Клинические состояния
    if result.get("clinical_conditions"):
        text += msg["conditions_header"] + "\n"
        for condition in result["clinical_conditions"]:
            text += msg["condition_item"].format(
                condition=condition.get("condition", "N/A"),
                severity=condition.get("severity", "N/A"),
                note=condition.get("note", "")
            ) + "\n"
    
    # Предупреждения
    if result.get("safety_warnings"):
        text += msg["warnings_header"] + "\n"
        for warning in result["safety_warnings"]:
            text += msg["warning_item"].format(warning=warning) + "\n"
    
    # Disclaimer
    if result.get("disclaimer"):
        
        subjective_note = {
            "ru": "\n\nℹ️ Примечание: Если данные холестерина/сахара введены без анализов, точность может быть ниже.",
            "en": "\n\nℹ️ Note: If cholesterol/glucose data were entered without lab tests, accuracy may be lower.",
            "kr": "\n\nℹ️ 참고: 콜레스테롤/혈당 데이터를 혈액 검사 없이 입력한 경우 정확도가 낮아질 수 있습니다."
        }
        text += subjective_note.get(lang, subjective_note["en"])
        text += msg["disclaimer"].format(text=result["disclaimer"])
          
    return text

async def send_result_with_buttons(update: Update, message: str, lang: str):
    """Отправка результата с кнопками для быстрых действий"""
    
    msg = MESSAGES[lang]
    
    # Создаем кнопки
    keyboard = [
        [KeyboardButton(msg["btn_new_analysis"])],
        [KeyboardButton(msg["btn_stats"]), KeyboardButton(msg["btn_help"])]
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    # Отправляем результат
    await update.message.reply_text(message)
    
    # Отправляем предложение действий с кнопками
    await update.message.reply_text(
        msg["after_result"],
        reply_markup=reply_markup
    )
# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================

def main():
    """Запуск бота"""
    
    # Проверка токена
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ОШИБКА: Установите TELEGRAM_BOT_TOKEN!")
        print("Получите токен у @BotFather в Telegram")
        print("Затем установите переменную окружения:")
        print("export TELEGRAM_BOT_TOKEN='ваш_токен'")
        return
    
    # Создание приложения
    from telegram.request import HTTPXRequest

    request = HTTPXRequest(
        connection_pool_size=8,
        read_timeout=100,
        write_timeout=60,
        connect_timeout=60,
        pool_timeout=60,
    )

    application = Application.builder().token(BOT_TOKEN).request(request).build()
    
    # Conversation handler для сбора данных
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(r"^(🔄 Новый анализ|🔄 New Analysis|🔄 새 분석)$"), start)
        ],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_choice)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_input)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender_input)],
            AP_HI: [MessageHandler(filters.TEXT & ~filters.COMMAND, ap_hi_input)],
            AP_LO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ap_lo_input)],
            CHOLESTEROL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cholesterol_input)],
            GLUCOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, glucose_input)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, height_input)], 
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, weight_input)], 
            SMOKE: [MessageHandler(filters.TEXT & ~filters.COMMAND, smoke_input)],
            ALCOHOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, alcohol_input)],
            ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, activity_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    # ==========================================
    # ОБРАБОТЧИК КНОПОК БЫСТРЫХ ДЕЙСТВИЙ
    # ==========================================
    
    async def handle_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатия на кнопки быстрых действий"""
        
        text = update.message.text
        lang = context.user_data.get('language', 'ru')
        
        # Проверяем какая кнопка нажата
        if any(keyword in text for keyword in ["📊", "статистика", "Statistics", "통계"]):
            # Кнопка "Статистика"
            await stats_command(update, context)
            return ConversationHandler.END
        
        elif any(keyword in text for keyword in ["❓", "Помощь", "Help", "도움말"]):
            # Кнопка "Помощь"
            await help_command(update, context)
            return ConversationHandler.END
        
        # Если текст не распознан - игнорируем
        return ConversationHandler.END
    
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_button_press))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Запуск бота
    print("✅ Бот запущен!")
    print(f"📊 Лимит: {DAILY_LIMIT} анализов в день")
    print(f"⏱ Rate limit: {RATE_LIMIT_MINUTES} минута между запросами")
    print(f"🌐 API: {API_URL}")
    print("\nБот работает... Нажмите Ctrl+C для остановки")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
