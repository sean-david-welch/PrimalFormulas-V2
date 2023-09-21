from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException

from models.models import User

from utils.security import (
    is_superuser,
    hash_password,
)
from database.users import create_user, update_user, delete_user, get_user

router = APIRouter()


@router.post("/create-user")
async def register(user: User):
    existing_user = await get_user(user.username)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username already exists!")

    try:
        user.password = hash_password(user.password)

        result = await create_user(user)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
    except Exception as error:
        return {"Error": str(error)}, 500

    return result


@router.put("/update-user/{user_id}")
async def update_user_account(user_id: str, user: User):
    current_user = await is_superuser()

    if current_user.role.value == "superuser":
        user_data = user.model_dump(exclude_unset=True)
        user_data["password"] = hash_password(user_data.pop("password"))

        result = await update_user(user_data, user_id)

        return result


@router.delete("/delete-user/{user_id}")
async def delete_user_account(user_id: str):
    current_user = await is_superuser()

    try:
        if current_user.role.value == "superuser":
            result = await delete_user(user_id)
            return result
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
