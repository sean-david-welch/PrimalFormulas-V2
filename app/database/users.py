from typing import List
from models.models import User
from database.database import (
    collections,
    database_handle_errors,
    database_insert_one,
    database_find_all,
    database_update_one,
    database_delete_one,
    handle_http_error,
)

from fastapi.exceptions import HTTPException

user_collections = collections["users"]


async def get_user(username: str) -> User:
    try:
        result = await user_collections.find_one(
            {"username": username} or {"email": username}
        )
    except Exception as error:
        database_handle_errors(error)

    user = User(**result)
    return user

    # return user.model_dump(exclude="password")


async def get_all_users() -> List[User]:
    try:
        result = database_find_all(user_collections)

    except HTTPException as error:
        handle_http_error(error)

    if result:
        return result


async def create_user(user: User) -> User:
    try:
        result = await database_insert_one(user_collections, user)

    except HTTPException as error:
        handle_http_error(error)

    if result:
        return user.model_dump()


async def update_user(user: User, user_id: str) -> User:
    try:
        result = await database_update_one(user_id, user, user_collections)

    except HTTPException as error:
        handle_http_error(error)

    if result:
        return user.model_dump()


async def delete_user(user_id: str) -> None:
    try:
        result = await database_delete_one(user_id)

    except HTTPException as error:
        handle_http_error(error)

    if result:
        return {"Message": f"User with id {user_id} has been deleted"}
