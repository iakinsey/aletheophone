from abc import ABC
from typing import Optional, TypeVar
from aiosqlite import Connection
from ..model.base import DataModel

T = TypeVar("T")


class DataGateway(ABC):
    db: Connection

    def __init__(self, db: Connection):
        self.db = db

    async def declare(self, model: DataModel):
        for q in model.schema().split(";"):
            if not q:
                continue

            await self.db.execute(q)
            await self.db.commit()

    async def fetch(self, Model: T, query: str, args: tuple = ()) -> list[T]:
        results = []

        async with self.db.execute(query, args) as cursor:
            async for row in cursor:
                results.append(Model.from_row(row))

        return results

    async def fetch_one(
        self, Model: T, query: str, args: tuple = (), commit=False
    ) -> Optional[T]:
        async with self.db.execute(query, args) as cursor:
            row = await cursor.fetchone()

        if commit:
            await self.db.commit()

        return Model.from_row(row)

    async def insert(self, query: str, args: list[tuple] = []):
        await self.db.executemany(query, args)
        await self.db.commit()

    async def execute(self, query: str, args: tuple = ()):
        await self.db.execute(query, args)
        await self.db.commit()
