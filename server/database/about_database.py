import logging

from models.about_models import About
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_abouts() -> list[About]:
    query = "SELECT * FROM about"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)

            rows = await cursor.fetchall()
            colums = [desc[0] for desc in cursor.description]

            return [
                About(**dict(zip(colums, row))).model_dump(mode="json") for row in rows
            ]
    except Exception as error:
        logger.error(f"An error occurred in get abouts: {error}", exc_info=True)
        return None


async def create_about(about: About) -> bool:
    query = "INSERT INTO about (title, description, image) VALUES (%s, %s, %s)"
    values = (about.title, about.description, about.image)

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)

            return True
    except Exception as error:
        logger.error(f"an error occurred while creating a about: {error}")
        return None


async def update_about(id: str, about: About) -> bool:
    if about.image and about.image.lower() != "null":
        query = (
            "UPDATE about SET title = %s, description = %s, image = %s WHERE id = %s"
        )
        values = (
            about.title,
            about.description,
            about.image,
            id,
        )
    else:
        query = "UPDATE about set title = %s, description = %s WHERE id = %s"
        values = (about.title, about.description, id)

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)
            return True
    except Exception as error:
        logger.error(f"an error occurred while updating a about: {error}")
        return None


async def delete_about(id: str) -> bool:
    query = "DELETE FROM about WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, [id])

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a about: {error}")
        return None
