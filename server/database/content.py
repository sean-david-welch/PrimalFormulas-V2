import logging

from uuid import uuid4
from datetime import datetime

from models.models import Content
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_content() -> list[Content]:
    query = "SELECT * FROM content"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

            return [
                Content(id=row[0], title=row[1], media=row[3], created=row[4])
                for row in rows
            ]
    except Exception as error:
        logger.error(f"An error occurred in get_products: {error}", exc_info=True)
        return None
