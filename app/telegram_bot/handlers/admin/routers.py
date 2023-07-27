from aiogram import Router

from app.telegram_bot.handlers.admin import add_chat_log, get_user_data


router = Router()
files = (add_chat_log, get_user_data)

for file in files:
    router.include_router(file.router)
