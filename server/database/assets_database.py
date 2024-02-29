import logging

from models.asset_models import Asset
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_assets() -> list[Asset]:
    query = "SELECT * FROM assets"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)

            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            return [Asset(**dict(zip(columns, row))) for row in rows]
    except Exception as error:
        logger.error(f"An error occurred in get_products: {error}", exc_info=True)
        return None


async def get_asset_by_title(title: str) -> Asset:
    query = "SELECT * FROM assets WHERE title = %s"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query, (title))
            asset = await cursor.fetchone()

            return Asset(*asset) if asset is not None else None
    except Exception as error:
        logger.error(f"An error occurred in get asset by title: {error}", exc_info=True)
        return None


async def create_asset(asset: Asset) -> bool:
    query = "INSERT INTO assets (title, media) VALUES (%s, %s)"
    values = (asset.title, asset.media)

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)
            return True
    except Exception as error:
        logger.error(
            f"an error occurred while creating the asset: {error}", exc_info=True
        )


async def update_asset(id: str, asset: Asset) -> bool:
    query = "UPDATE assets SET title = %s, media = %s WHERE id = %s"
    values = (
        asset.title,
        asset.media,
        id,
    )

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)
            return True
    except Exception as error:
        logger.error(f"an error occurred while updating a asset: {error}")
        return None


async def delete_asset(id: str) -> bool:
    query = "DELETE FROM assets WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, [id])

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a asset: {error}")
        return None
