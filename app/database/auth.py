from models.models import User
from database.database import collections, database_handle_errors

user_collections = collections["users"]


async def create_user(user: User) -> User:
    user_data = user.model_dump()


async def get_user(username: str) -> User:
    try:
        user_data = await user_collections.find_one(
            {"username": username} or {"email": username}
        )
    except Exception as error:
        database_handle_errors(error)

    user = User(**user_data)
    return user.model_dump(exclude="password_hash")
