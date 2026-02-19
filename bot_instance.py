import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from aiogram.enums import ParseMode

# Initialize Bot and Dispatcher
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()
