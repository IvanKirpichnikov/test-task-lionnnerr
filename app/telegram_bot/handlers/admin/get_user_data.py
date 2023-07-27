from json import loads
from typing import TYPE_CHECKING

from aiogram import Router, html
from aiogram.types import CallbackQuery
from fluentogram import TranslatorRunner
from redis.asyncio import Redis

from app.infrastructure.database.models.user import UserOrderModel, UserDataModel
from app.telegram_bot.keyboards.admin.inline import UserData

if TYPE_CHECKING:
    from stubs import TranslatorRunner


router = Router()

@router.callback_query(UserData.filter())
async def set_user_data(
    callback: CallbackQuery,
    callback_data: UserData,
    redis: Redis,
    l10n: TranslatorRunner
) -> None:
    redis_key = callback_data.redis_key
    data = loads(await redis.get(redis_key))

    user_data = UserDataModel(**data.get('user_data'))
    user_order = UserOrderModel(
        user_data=user_data,
        text=data.get('text')
    )
    
    await callback.message.edit_text(
        text=l10n.user.order.data(
            tid=str(user_data.tid),
            username=user_data.username,
            datetime=user_data.datetime,
            phone_number=user_data.phone_number,
            email=user_data.email,
            order_text=html.quote(user_order.text)
        )
    )



