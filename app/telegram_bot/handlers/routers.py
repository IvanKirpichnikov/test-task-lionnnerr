from aiogram import Router

from app.telegram_bot.handlers.admin import routers as a_routers
from app.telegram_bot.handlers.dev import routers as d_routers
from app.telegram_bot.handlers.user import routers as u_routers

router = Router()
files = (u_routers, a_routers, d_routers)

for file in files:
    router.include_router(file.router)
