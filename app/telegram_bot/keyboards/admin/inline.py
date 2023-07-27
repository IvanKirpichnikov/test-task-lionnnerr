from typing import TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, CallbackData
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from stubs import TranslatorRunner


class UserData(CallbackData, prefix='user_data'):
    """:param redis_key: redis ключ получения информации о юзере"""
    redis_key: str


def keyboard_get_user_data(
    l10n: TranslatorRunner,
    redis_key: str
) -> InlineKeyboardMarkup:
    """
    :param l10n: fluentogram.TranslatorRunner локали
    :maram redis_ket: redis ключ получения информации о юзере
    """
    bilder = InlineKeyboardBuilder()
    
    bilder.button(
        text=l10n.button.gett.info(),
        callback_data=UserData(redis_key=redis_key)
    )
    
    return bilder.as_markup()
