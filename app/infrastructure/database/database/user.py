from logging import getLogger

from asyncpg import Connection

from app.infrastructure.database.database.base import BaseDB
from app.infrastructure.database.models.user import UserDataModel

logger = getLogger(__name__)


class _UserDB(BaseDB):
    table_name = 'users'
    
    def __init__(self, connect: Connection) -> None:
        self.connect = connect
    
    async def create_table(self) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    tid BIGINT UNIQUE,
                    cid BIGINT UNIQUE,
                    datetime TIMESTAMPTZ DEFAULT now()
                );
            ''')
            logger.info("Created table '%s'", self.table_name)
    
    async def add(self, *, tid: int, cid: int) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                INSERT INTO users(tid, cid)
                VALUES($1, $2) ON CONFLICT DO NOTHING;
            ''', tid, cid
            )
            logger.info(
                "Add user. db='%s', tid='%d', cid='%d'",
                self.table_name, tid, cid
            )
    
    async def delete(self, *, tid: int) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                DELETE FROM users WHERE tid = $1;
            ''', tid
            )
            logger.info(
                "Delete user. db='%s', tid='%d'",
                self.table_name, tid
            )
    
    async def get(self, *, tid: int) -> UserDataModel:
        async with self.connect.transaction():
            cursor = await self.connect.cursor('''
                SELECT users.id,
                       users.tid,
                       users.cid,
                       TO_CHAR(
                           users.datetime,
                           'DD.MM.YYYY HH24:MI:SS'
                       ) datetime,
                       data.phone_number,
                       data.email
                FROM users, data
                WHERE users.tid = $1
            ''', tid
            )
            data = await cursor.fetchrow()
            return UserDataModel(**data)
