import logging

from models.models import Product
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_products() -> list[Product]:
    query = "SELECT * FROM products"

    try:
        async with pool.connection() as conn, conn.cursor() as curr:
            curr.execute(query)
            rows = curr.fetchall()

            return [
                Product(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    price=row[3],
                    image=row[4],
                    created=row[5],
                )
                for row in rows
            ]
    except Exception as error:
        logger.error(f"An error occurred in get_products: {error}", exc_info=True)
        return None
