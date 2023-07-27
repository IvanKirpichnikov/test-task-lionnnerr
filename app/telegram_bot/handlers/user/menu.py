from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from fluentogram import TranslatorRunner

from app.telegram_bot.keyboards.inline import keyboard_menu

if TYPE_CHECKING:
    from stubs import TranslatorRunner


router = Router()


@router.message(Command('menu'))
@router.message(CommandStart())
async def menu_message(
    message: Message,
    state: FSMContext,
    l10n: TranslatorRunner
) -> None:
    await message.answer(
        text=l10n.click(),
        reply_markup=keyboard_menu(l10n)
    )
    await state.clear()

@router.callback_query(F.data=='cancel')
async def menu_callback_query(
    callback: CallbackQuery,
    state: FSMContext,
    l10n: TranslatorRunner
) -> None:
    await callback.message.edit_text(
        text=l10n.click(),
        reply_markup=keyboard_menu(l10n)
    )
    await state.clear()
