from models.models import Static
from database.database import (
    collections,
    handle_http_error,
    database_insert_one,
    database_update_one,
    database_delete_one,
)
from fastapi.exceptions import HTTPException

static_collection = collections["static"]


async def get_static(title: str) -> Static:
    try:
        result = await static_collection.find_one({"title": title})

    except HTTPException as error:
        handle_http_error(error)

    return result


async def create_static(static: Static) -> Static:
    try:
        result = await database_insert_one(static_collection, static)
    except HTTPException as error:
        handle_http_error(error)

    if result:
        return static.model_dump()


async def update_static(static: Static, static_id: str) -> Static:
    try:
        result = await database_update_one(static_id, static, static_collection)
    except HTTPException as error:
        handle_http_error(error)

    if result:
        return static.model_dump()


async def delete_static(static_id: str) -> None:
    try:
        result = await database_delete_one(static_id, static_collection)
    except HTTPException as error:
        handle_http_error(error)

    if result:
        return {"Message": f"Static content with id {static_id} has been deleted"}
