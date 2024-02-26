from psycopg_pool import AsyncConnectionPool
from functools import lru_cache

from asyncio import sleep
from config import settings


@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=settings["DATABASE_URL"])


async def check_async_connection():
    while True:
        await sleep(600)
        await get_async_pool().check()
