from typing import TYPE_CHECKING

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from stubs import TranslatorRunner


def keyboard_menu(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()

    bilder.button(
        text=l10n.button.my.profile(),
        callback_data='my_profile'
    )
    bilder.button(
        text=l10n.button.order.an.order(),
        callback_data='order_an_order'
    )

    return bilder.adjust(1).as_markup()


def keyboard_cancel(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()

    bilder.button(
        text=l10n.button.cancel(),
        callback_data='cancel'
    )

    return bilder.as_markup()


def keyboard_my_profile(l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()

    bilder.button(
        text=l10n.button.edit.phone.number(),
        callback_data='edit_phone_number'
    )
    bilder.button(
        text=l10n.button.edit.email(),
        callback_data='edit_email'
    )
    bilder.button(
        text=l10n.button.cancel(),
        callback_data='cancel'
    )

    return bilder.adjust(2, 1).as_markup()


def keyboard_back_to_memu(str, l10n: TranslatorRunner) -> InlineKeyboardMarkup:
    bilder = InlineKeyboardBuilder()

    bilder.button(
        text=l10n.button.cancel(),
        callback_data='cancel'
    )

    return bilder.as_markup()
