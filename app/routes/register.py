from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from models.models import User

from utils.security import (
    get_current_user,
    hash_password,
)
from database.users import create_user, update_user, delete_user, get_user

router = APIRouter()


@router.post("/create-user")
async def register(user: User, current_user: User = Depends(get_current_user)):
    if current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission Denied")

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

    if current_user:
        return result


@router.put("/update-user/{user_id}")
async def update_user_account(
    user_id: str, user: User, current_user: User = Depends(get_current_user)
):
    if current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission Denied")

    try:
        user.password = hash_password(user.password)

        result = await update_user(user, user_id)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
    except Exception as error:
        return {"Error": str(error)}, 500

    return result


@router.delete("/delete-user/{user_id}")
async def delete_user_account(
    user_id: str, current_user: User = Depends(get_current_user)
):
    if current_user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission Denied")

    try:
        result = await delete_user(user_id)
        return result

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
