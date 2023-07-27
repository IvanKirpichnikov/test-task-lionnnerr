from aiogram import Router

from app.telegram_bot.handlers.dev import events_bot


router = Router(name=__name__)
files = (events_bot, )

for file in files:
    router.include_router(file.router)
