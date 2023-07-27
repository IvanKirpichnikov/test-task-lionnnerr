from aiogram import Router

from app.telegram_bot.handlers.admin import add_chat_log


router = Router()
files = (add_chat_log,)

for file in files:
    router.include_router(file.router)
