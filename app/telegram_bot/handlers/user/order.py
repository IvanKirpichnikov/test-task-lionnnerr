from dataclasses import asdict
from json import loads, dumps
from typing import TYPE_CHECKING

from aiogram import Bot, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from app.infrastructure.database.database.db import DB
from app.infrastructure.database.models.user import UserOrderModel
from app.telegram_bot.handlers.user.menu import menu_message
from app.telegram_bot.keyboards.admin.inline import keyboard_get_user_data
from app.telegram_bot.keyboards.inline import keyboard_cancel
from app.telegram_bot.states import Order
from app.telegram_bot.utils.random_key import random_key

if TYPE_CHECKING:
    from stubs import TranslatorRunner


router = Router()
LIMIT_ORDER_TEXT = 2000


@router.callback_query(F.data == 'order_an_order')
async def ask_order_text(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: TranslatorRunner
) -> None:
    await callback.message.edit_text(
        text=l10n.ask.order.text(),
        reply_markup=keyboard_cancel(l10n)
    )
    await state.set_state(Order.text)
    await callback.answer()


@router.message(Order.text, F.text.len() <= LIMIT_ORDER_TEXT)
async def get_order_text(
    message: Message,
    bot: Bot,
    state: FSMContext,
    redis: Redis,
    l10n: TranslatorRunner,
    db: DB
) -> None:
    await message.delete()
    
    redis_key = random_key()
    order_text = message.html_text
    log_chat_id = loads(await redis.get('log_chat_id'))
    username = f'@{message.from_user.username}' if message.from_user.username else ''
    user_data = await db.user.get(tid=message.from_user.id)
    user_data.username = username
    user_order = UserOrderModel(user_data=user_data, text=order_text)
    
    await message.answer(text=l10n.thanks.to.order())
    await bot.send_message(
        chat_id=log_chat_id,
        text=l10n.user.order.no.data(
            tid=str(message.from_user.id),
            username=username,
            order_text=order_text
        ),
        reply_markup=keyboard_get_user_data(l10n, redis_key)
    )

    await redis.set(redis_key, dumps(asdict(user_order)))
    await menu_message(message, state, l10n)
