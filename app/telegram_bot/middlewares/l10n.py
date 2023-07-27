from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from fluentogram import TranslatorHub


class L10NMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, any]], Awaitable[None]],
        event: Update,
        data: dict[str, any]
    ) -> any:
        user = data.get('event_from_user')
        
        if user is None:
            return await handler(event, data)

        hub: TranslatorHub = data.get('hub')
        data['l10n'] = hub.get_translator_by_locale(
            user.language_code
        )
        return await handler(event, data)
