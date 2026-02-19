from app.bot_instance import dp
from bot.handlers import common, form

import logging

from aiogram import types

# Register Routers
# This execution happens on import
dp.include_router(common.router)
dp.include_router(form.router)

# DEBUG: Catch-all handler to diagnose unhandled updates
@dp.message()
async def dbg_catch_all(message: types.Message):
    logging.warning(f"DEBUG: Unhandled message received: {message.text} from {message.from_user.id}")
logging.info(f"Bot routers registered: {len(dp.sub_routers)} routers active.")
