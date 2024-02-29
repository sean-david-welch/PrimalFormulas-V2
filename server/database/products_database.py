import logging

from models.products_models import Product, ProductMutation
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_products() -> list[Product]:
    query = "SELECT * FROM products"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)

            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            products = [
                Product(**dict(zip(columns, row))).model_dump(mode="json")
                for row in rows
            ]
            return products
    except Exception as error:
        logger.error(f"An error occurred in get_products: {error}", exc_info=True)
        return None


async def get_product_by_id(id: str) -> Product:
    query = "SELECT * FROM products WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query, [id])
            product = await cursor.fetchone()

            return Product(*product) if product is not None else None
    except Exception as error:
        logger.error(f"An error occurred in get_products_by_id: {error}", exc_info=True)
        return None


async def create_product(product: ProductMutation) -> bool:
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


async def update_product(id: str, product: ProductMutation) -> bool:
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


async def delete_product(id: str) -> bool:
    query = "DELETE FROM products WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, [id])

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a product: {error}")
        return None
