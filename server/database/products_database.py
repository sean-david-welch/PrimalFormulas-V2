import logging

from models.products_models import Product, ProductMutation
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_products() -> list[Product] | None:
    query = "SELECT * FROM products"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)

            rows = await cursor.fetchall()
            if rows is None:
                return None

            products = [
                Product(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    price=row[3],
                    image=row[4],
                )
                for row in rows
            ]

            return products
    except Exception as error:
        logger.error(f"An error occurred in get_products: {error}", exc_info=True)
        return None


async def get_product_by_id(id: str) -> Product | None:
    query = "SELECT * FROM products WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query, [id])
            row = await cursor.fetchone()

            if row is None:
                return None

            return Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                image=row[4],
            )
    except Exception as error:
        logger.error(f"An error occurred in get_products_by_id: {error}", exc_info=True)
        return None


async def create_product(product: ProductMutation) -> bool | None:
    query = (
        "INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)"
    )
    values = (
        product.name,
        product.description,
        product.price,
        product.image,
    )

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)
            return True
    except Exception as error:
        logger.error(f"an error occurred while creating a product: {error}")
        return None


async def update_product(id: str, product: ProductMutation) -> bool | None:
    if product.image and product.image.lower() != "null":
        query = "UPDATE products SET name = %s, description = %s, price = %s, image = %s WHERE id = %s"
        values = (
            product.name,
            product.description,
            product.price,
            product.image,
            id,
        )
    else:
        query = (
            "UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s"
        )
        values = (
            product.name,
            product.description,
            product.price,
            id,
        )

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)
            return True
    except Exception as error:
        logger.error(f"an error occurred while updating a product: {error}")
        return None


async def delete_product(id: str) -> bool | None:
    query = "DELETE FROM products WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, [id])

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a product: {error}")
        return None
