import logging

from uuid import uuid4
from datetime import datetime

from models.models import About
from utils.database import get_async_pool

pool = get_async_pool()
logger = logging.getLogger()


async def get_abouts() -> list[About]:
    query = "SELECT * FROM about"

    try:
        async with pool.connection() as conn, conn.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

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


async def create_about(about: About) -> bool:
    about.id = uuid4()
    about.created = datetime.now()

    query = "INSERT INTO about (id, title, description, image, created) VALUES (%s, %s, %s, %s, %s)"
    values = (about.id, about.title, about.description, about.image, about.created)

    try:
        async with pool.connection() as conn, conn.transaction():
            await conn.execute(query, values)

            return True
    except Exception as error:
        logger.error(f"an error occurred while creating a about: {error}")
        return None


async def update_about(id: str, about: About) -> bool:
    query = "UPDATE about SET name = %s, description = %s, image = %s WHERE id = %s"
    values = (
        about.title,
        about.description,
        about.image,
        id,
    )

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
            await conn.execute(query(id))

            return True
    except Exception as error:
        logger.error(f"an error occurred while deleting a about: {error}")
        return None
