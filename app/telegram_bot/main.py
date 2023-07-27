from logging import getLogger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from asyncpg import Pool
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from app.telegram_bot.handlers.routers import router
from app.telegram_bot.middlewares.database import DataBaseMiddleware
from app.telegram_bot.middlewares.l10n import L10NMiddleware
from app.telegram_bot.middlewares.throttling import ThrottlingMiddleware
from config import Config

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
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(
            with_destiny=True
        )
    )
    dp = Dispatcher(
        storage=storage,
        events_isolation=storage.create_isolation()
    )
    logger.debug('Setups middlewares')
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(L10NMiddleware())
    
    logger.debug('Setups kwargs')
    dp['pool'] = pool
    dp['redis'] = redis
    dp['hub'] = hub
    dp['config'] = config
    
    logger.debug('setup routers')
    dp.include_router(router)
    
    allowed_updates=dp.resolve_used_update_types()
    
    logger.warning('Start telegram bot')
    logger.warning('Updates=%s', allowed_updates)
    
    await dp.start_polling(
        bot, allowed_updates=allowed_updates
    )
