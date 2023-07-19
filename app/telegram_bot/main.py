from logging import getLogger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisEventIsolation, RedisStorage
from asyncpg import Pool
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from config import Config
from app.telegram_bot.middlewares.database import DataBaseMiddleware
from app.telegram_bot.middlewares.l10n import L10NMiddleware
from app.telegram_bot.middlewares.trottling import TrottlingMiddleware


logger = getLogger(__name__)


async def start_telegram_bot(
    pool: Pool,
    redis: Redis,
    hub: TranslatorHub,
    config: Config
) -> None:
    bot = Bot(
        config.bot.token.get_secret_value(),
        parse_mode=ParseMode.HTML.value
    )
    await bot.delete_webhook(
        drop_pending_updates=config.bot.skip_updates
    )
    
    dp = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(
                with_destiny=True
            )
        ),
        events_isolation=RedisEventIsolation(redis=redis)
    )
    logger.info('Setups middlewares')
    dp.message.middleware(TrottlingMiddleware())
    dp.callback_query.middleware(TrottlingMiddleware())
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(L10NMiddleware())
    
    logger.info('Setups kwargs')
    dp['pool'] = pool
    dp['redis'] = redis
    dp['hub'] = hub
    
    allowed_updates=dp.resolve_used_update_types()
    
    logger.info('Start telegram bot')
    logger.info('Updates=%s', *allowed_updates)
    
    await dp.start_polling(
        bot, allowed_updates=allowed_updates
    )
