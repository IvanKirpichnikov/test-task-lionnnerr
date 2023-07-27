from logging import getLogger

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, IS_ADMIN
from aiogram.types import ChatMemberUpdated
from redis.asyncio import Redis

from config import Config


router = Router(name=__name__)
logger = getLogger()


@router.my_chat_member(
    ChatMemberUpdatedFilter(IS_ADMIN),
    F.chat.type.in_(
        {ChatType.GROUP.value,
         ChatType.SUPERGROUP.value}
    )
)
async def add_bot_for_chat(
    event: ChatMemberUpdated,
    config: Config,
    redis: Redis
) -> None:
    user_id = event.from_user.id

    if user_id != config.bot.owner_id:
        await event.chat.leave()
        return
    logger.info(
        'The bot was added to the group for logs. ChatID=%s',
        event.chat.id
    )
    await redis.set('log_chat_id', event.chat.id)
