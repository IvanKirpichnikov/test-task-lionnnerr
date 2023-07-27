from aiogram import Router

from app.telegram_bot.handlers.user import menu, order, profile


router = Router()
files = (menu, order, profile)

for file in files:
    router.include_router(file.router)
