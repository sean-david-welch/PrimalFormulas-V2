from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from models.models import AboutContent, User
from utils.security import get_current_user
from database.about import get_all_abouts, create_about, update_about, delete_about

router = APIRouter()


@router.get("", response_model=list[AboutContent])
async def get_about_content():
    try:
        response = await get_all_abouts()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("")
async def post_about_content(
    about: AboutContent, user: User = Depends(get_current_user)
) -> AboutContent:
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await create_about(about)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}")
async def put_about_content(
    about: AboutContent, id: str, user: User = Depends(get_current_user)
) -> AboutContent:
    if not user.role == "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await update_about(about, id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}")
async def delete_about_content(id: str, user: User = Depends(get_current_user)) -> None:
    if not user.role == "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await delete_about(id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
