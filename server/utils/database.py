from psycopg_pool import AsyncConnectionPool
from functools import lru_cache

from config import settings


@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=settings["DATABASE_URL"])
