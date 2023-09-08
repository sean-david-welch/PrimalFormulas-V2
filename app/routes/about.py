from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from models.models import AboutContent
from database.about import get_all_abouts, create_about, update_about, delete_about

router = APIRouter()


@router.get("/")
async def get_about_content():
    try:
        response = await get_all_abouts()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("/")
async def post_about_content(about: AboutContent) -> AboutContent:
    try:
        response = await create_about(about)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}")
async def put_about_content(about: AboutContent, about_id: str) -> AboutContent:
    try:
        response = await update_about(about, about_id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}")
async def delete_about_content(about_id: str) -> None:
    try:
        response = await delete_about(about_id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
