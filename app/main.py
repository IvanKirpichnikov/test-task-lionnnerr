import asyncio

from asyncpg import Connection, create_pool
from fluent_compiler.bundle import FluentBundle
from fluentogram import TranslatorHub, FluentTranslator
from redis.asyncio import Redis

from config import Config


async def run():
   config = Config()
   redis = config.redis
   psql = config.psql
   
   hub = TranslatorHub(
       dict(
           ru=('ru',)
       ),
       list(
           FluentTranslator(
               'ru',
               translator=FluentBundle.from_files(
                   'ru_RU',
                   filenames=['locales/ru/text.ftl']
               )
           )
       ),
       root_locale='ru'
   )
   pool = await create_pool(
       user=psql.user,
       password=psql.password.get_secret_value(),
       host=psql.host,
       port=psql.port,
       database=psql.database,
       auto
   )
   redis = Redis(
       host=redis.host,
       port=redis.port,
       password=redis.password.get_secret_value(),
       db=redis.database
   )
   
