from app.bot_instance import dp
from bot.handlers import common, form

# Register Routers
# This execution happens on import
dp.include_router(common.router)
dp.include_router(form.router)
