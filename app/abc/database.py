from abc import ABC, abstractmethod

from asyncpg import Connection


class AbstractDB(ABC):
    def __init__(self, connect: Connection):
        pass
    
    @abstractmethod
    async def create_table(self) -> None:
        pass
