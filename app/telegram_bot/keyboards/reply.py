from typing import TYPE_CHECKING

from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from stubs import TranslatorRunner


def keyboard_ask_phone_number(l10n: TranslatorRunner) -> ReplyKeyboardMarkup:
    bilder = ReplyKeyboardBuilder()
    
    bilder.button(
        text=l10n.button.ask.phone.number(),
        request_contact=True
    )
    
    return bilder.as_markup(
        resize_keyboard=True,
    )
