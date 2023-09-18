from typing import List
from models.models import AboutContent
from database.database import (
    collections,
    handle_http_error,
    database_find_all,
    database_insert_one,
    database_update_one,
    database_delete_one,
)
from pydantic import ValidationError
from fastapi.exceptions import HTTPException


about_collection = collections["about"]


async def get_all_abouts() -> List[AboutContent]:
    about_data = await database_find_all(about_collection)

    if not about_data:
        raise HTTPException(status_code=404, detail="Couldn't find data")

    return about_data


async def create_about(about: AboutContent) -> AboutContent | HTTPException:
    try:
        result = await database_insert_one(about_collection, about)
    except ValidationError as error:
        handle_http_error(error)
    return result


async def update_about(
    about: AboutContent, about_id: str
) -> AboutContent | HTTPException:
    try:
        result = await database_update_one(about_id, about, about_collection)
    except ValidationError as error:
        handle_http_error(error)

    return result


async def delete_about(about_id: str) -> None:
    try:
        result = await database_delete_one(about_id, about_collection)
    except ValidationError as error:
        handle_http_error(error)

    return result
