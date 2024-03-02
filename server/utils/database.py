import logging

from functools import lru_cache
from psycopg_pool import AsyncConnectionPool

from utils.config import settings

logger = logging.getLogger()


@lru_cache()
def get_async_pool() -> AsyncConnectionPool:
    if not settings.get("DATABASE_URL"):
        raise Exception("DATABASE_URL not set")

    return AsyncConnectionPool(conninfo=settings.get("DATABASE_URL", ""))
