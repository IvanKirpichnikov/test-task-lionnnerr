from typing import TYPE_CHECKING

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.infrastructure.database.database.db import DB
from app.telegram_bot.filters.check_phone_number import CheckPhoneNumber
from app.telegram_bot.keyboards.inline import keyboard_my_profile
from app.telegram_bot.keyboards.reply import keyboard_ask_phone_number
from app.telegram_bot.states import MyProfile

if TYPE_CHECKING:
    from stubs import TranslatorRunner


router = Router()


@router.message(Command('menu'))
async def my_profile_message(
    message: Message,
    state: FSMContext,
    l10n: TranslatorRunner,
    db: DB
) -> None:
    username = f'@{message.from_user.username}' if message.from_user.username else ''

    data = await db.user.get(tid=message.from_user.id)
    await message.answer(
        text=l10n.my.profile(
            email=data.email,
            datetime=data.datetime,
            tid=str(data.tid),
            phone_number=data.phone_number,
            username=username
         ),
        reply_markup=keyboard_my_profile(l10n)
    )
    await state.clear()

@router.callback_query(F.data.in_({'my_profile', 'back_to_my_profile'}))
async def my_profile_callback_query(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: TranslatorRunner,
    db: DB
) -> None:
    username = f'@{callback.from_user.username}' if callback.from_user.username else ''

    data = await db.user.get(tid=callback.from_user.id)
    await callback.message.edit_text(
        text=l10n.my.profile(
            email=data.email,
            datetime=data.datetime,
            tid=str(data.tid),
            phone_number=data.phone_number,
            username=username
         ),
        reply_markup=keyboard_my_profile(l10n)
    )
    await state.clear()

@router.callback_query(F.data=='edit_phone_number')
async def ask_new_phone_number(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: TranslatorRunner
) -> None:
    await callback.message.delete()
    msg = await callback.message.answer(
        l10n.edit.phone.number(),
        reply_markup=keyboard_ask_phone_number(l10n)
    )
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(MyProfile.phone_number)

@router.message(MyProfile.phone_number, CheckPhoneNumber())
async def get_new_phone_number(
    message: Message,
    bot: Bot,
    state: FSMContext,
    l10n: TranslatorRunner,
    db: DB,
    phone_number: str
) -> None:
    data = await state.get_data()
    await message.delete()
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=data.get('msg_id')
    )
    await db.data.update_phone_number(
        tid=message.from_user.id,
        phone_number=phone_number
    )
    await my_profile_message(message, state, l10n, db)

@router.callback_query(F.data == 'edit_email')
async def ask_new_email(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: TranslatorRunner
) -> None:
    await callback.message.edit_text(text=l10n.edit.email())
    await state.set_state(MyProfile.email)

@router.message(MyProfile.email, F.entities[...].type == 'email')
async def get_new_email(
    message: Message,
    state: FSMContext,
    l10n: TranslatorRunner,
    db: DB
) -> None:
    email = [
        data.extract_from(message.text)
        for data in message.entities
        if data.type == 'email'
    ][-1]
    await message.delete()
    await db.data.update_email(
        tid=message.from_user.id,
        email=email
    )
    await my_profile_message(message, state, l10n, db)
