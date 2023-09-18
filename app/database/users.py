from models.models import User
from database.database import (
    collections,
    database_handle_errors,
    database_insert_one,
    database_find_one,
    database_find_all,
    database_update_one,
    database_delete_one,
    handle_http_error,
)

from pydantic import ValidationError
from fastapi.exceptions import HTTPException

user_collections = collections["users"]


async def get_user(username: str) -> User:
    try:
        user_data = await user_collections.find_one(
            {"username": username} or {"email": username}
        )
    except Exception as error:
        database_handle_errors(error)

    user = User(**user_data)
    return user.model_dump(exclude="password_hash")


async def create_user(user: User) -> User:
    try:
        result = await database_insert_one(user_collections, user)
    except ValidationError as error:
        handle_http_error(error)
    return result
