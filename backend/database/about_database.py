import logging

from models.about_models import About, AboutMutation
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_abouts() -> list[About] | None:
    query = "SELECT * FROM about"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)

            rows = await cursor.fetchall()

            if rows is None:
                return None

            return [
                About(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    image=row[3],
                    created=row[4],
                )
                for row in rows
            ]
    except Exception as error:
        logger.error(f"An error occurred in get abouts: {error}", exc_info=True)
        return None


async def create_about(about: AboutMutation) -> bool | None:
    query = "INSERT INTO about (title, description, image) VALUES (%s, %s, %s)"
    values = (about.title, about.description, about.image)

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)

            return True
    except Exception as error:
        logger.error(f"an error occurred while creating a about: {error}")
        return None


async def update_about(id: str, about: AboutMutation) -> bool | None:
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


async def delete_about(id: str) -> bool | None:
    query = "DELETE FROM about WHERE id = %s"

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, [id])

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a about: {error}")
        return None
