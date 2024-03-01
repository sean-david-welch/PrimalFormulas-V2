import logging

from functools import lru_cache

from psycopg_pool import AsyncConnectionPool

from utils.config import settings

logger = logging.getLogger()


@lru_cache()
def get_async_pool():
    logger.info(f"database url {settings["DATABASE_URL"]}")
    return AsyncConnectionPool(conninfo=settings["DATABASE_URL"])
