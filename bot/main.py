import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.handlers import common, form

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not defined. Please check your .env file or config.")
        return

    # Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Include Routers
    dp.include_router(common.router)
    dp.include_router(form.router)

    logging.info("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
