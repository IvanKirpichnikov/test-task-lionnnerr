from typing import Awaitable, Callable, Union, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.8):
        self.cache: Dict[int, None] = TTLCache(maxsize=10000, ttl=rate_limit)
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, any]], Awaitable[None]],
        event: Union[Message, CallbackQuery],
        data: dict[str, any]
    ) -> any:
        user = data.get('event_from_user')
        
        if user is None:
            return await handler(event, data)
        if user.id in self.cache:
            return
        self.cache[user.id] = None
        
        return await handler(event, data)
