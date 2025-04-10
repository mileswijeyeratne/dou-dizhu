import psycopg
from psycopg_pool import AsyncConnectionPool

from contextlib import asynccontextmanager

from typing import AsyncGenerator, Sequence, Any, TypeVar, Type

DATABASE_URI = "postgresql://postgres:g1raffe@database:5432/postgres"

T = TypeVar("T")

class Database:
    def __init__(self) -> None:
        self.pool: AsyncConnectionPool | None = None 

    async def open_pool(self):
        self.pool = AsyncConnectionPool(DATABASE_URI, open=False)
        await self.pool.open()

    async def close_pool(self):
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def get_conn(self) -> AsyncGenerator[psycopg.AsyncConnection, None]:
        if self.pool is None:
            raise RuntimeError("Pool has not been opened, call `open_pool()` first.")
        async with self.pool.connection() as conn:
            yield conn

    async def fetchone(
        self,
        query: str,
        args: Sequence[Any],
        datatype: Type[T],
    ) -> T | None:
        async with self.get_conn() as conn:
            cursor: psycopg.AsyncCursor[T]
            async with conn.cursor(row_factory=psycopg.rows.class_row(datatype)) as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchone()

    async def fetchmany(
        self,
        query: str,
        args: Sequence[Any],
        size: int,
        datatype: Type[T],
    ) -> list[T]:
        async with self.get_conn() as conn:
            cursor: psycopg.AsyncCursor[T]
            async with conn.cursor(row_factory=psycopg.rows.class_row(datatype)) as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchmany(size)

    async def fetchall(
        self,
        query: str,
        args: Sequence[Any],
        datatype: Type[T],
    ) -> list[T]:
        async with self.get_conn() as conn:
            cursor: psycopg.AsyncCursor[T]
            async with conn.cursor(row_factory=psycopg.rows.class_row(datatype)) as cursor:
                await cursor.execute(query, args)
                return await cursor.fetchall()

    async def execute(
        self,
        query: str,
        args: Sequence[Any],
        commit: bool = True
    ) -> None:
        async with self.get_conn() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)
                if commit:
                    await conn.commit()
