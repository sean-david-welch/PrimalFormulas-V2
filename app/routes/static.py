from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from models.models import Static, User
from utils.security import get_current_user
from database.static import create_static, get_static, update_static, delete_static

router = APIRouter()


@router.get("/{name}", response_model=Static)
async def get_static_content(title: str) -> Static | HTTPException:
    response = await get_static(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Content: {title} not found!")


@router.post("/", response_model=Static)
async def post_static_content(
    static: Static, user: User = Depends(get_current_user)
) -> Static | HTTPException:
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await create_static(static)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}", response_model=None)
async def update_static_content(
    static_id: str, static: Static, user: User = Depends(get_current_user)
) -> Static | HTTPException:
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await update_static(static, static_id)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}", response_model=Static)
async def delete_static_content(
    static_id: str, user: User = Depends(get_current_user)
) -> Static | HTTPException:
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await delete_static(static_id)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
