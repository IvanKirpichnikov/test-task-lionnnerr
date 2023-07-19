from logging import getLogger

from asyncpg import Connection

from app.infrastructure.database.database.db import DB


logger = getLogger(__name__)


async def create_tables(connect: Connection) -> None:
    db = DB(connect)
    
    await db.user.create_table()
    logger.info("Created 'user' table")
    await db.data.create_table()
    logger.info("Created 'data' table")
