from logging import getLogger

from asyncpg import create_pool, Pool
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
from redis.asyncio import Redis

from config import Config
from app.infrastructure.database.utils.create_tables import create_tables
from app.telegram_bot.main import start_telegram_bot


logger = getLogger(__name__)


async def close(redis: Redis, pool: Pool) -> None:
    await redis.close()
    logger.info('Close redis')
    await pool.close()
    logger.info('Close postgresql pool')

async def run():
    config = Config()
    redis = config.redis
    psql = config.psql
    
    hub = TranslatorHub(
        dict(
            ru=('ru',)
        ),
        [
            FluentTranslator(
                'ru',
                translator=FluentBundle.from_files(
                    'ru_RU',
                    filenames=['locales/ru/text.ftl']
                )
            )
        ],
        root_locale='ru'
    )
    logger.info('Created TranslatorHub')
    pool = await create_pool(
        user=psql.user,
        password=psql.password.get_secret_value(),
        host=psql.host,
        port=psql.port,
        database=psql.database
    )
    logger.info('Created postgresql pool. Pool=%s', pool)
    redis = Redis(
        encoding='utf-8',
        host=redis.host,
        port=redis.port,
        password=redis.password.get_secret_value(),
        db=redis.database
    )
    logger.info('Created redis connect. Connect=%s', redis)
    
    async with pool.acquire() as connect:
        try:
            await create_tables(connect)
        except Exception as e:
            logger.exception(e)
            await close(redis, pool)
    
    try:
        await start_telegram_bot(
            pool=pool,
            redis=redis,
            hub=hub,
            config=config
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await close(redis, pool)
