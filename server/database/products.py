import psycopg

from models.models import Product
from utils.config import settings


async def get_products() -> list[Product]:
    query = "SELECT * FROM products"
    database_url = settings["DATABASE_URL"]

    try:
        async with psycopg.AsyncConnection.connect(database_url) as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                rows = await cur.fetchall()
                # Assuming you have a way to convert rows to Product instances
                products = [Product(**row) for row in rows]
                return products
    except Exception as err:
        # Consider logging the error here
        return []  # Return an empty list or consider raising the exception
