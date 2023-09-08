from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from models.models import Static
from database.static import create_static, get_statc, update_static, delete_static

router = APIRouter()


@router.post(
    "/",
    response_model=Static,
)
async def post_static_content(static: Static):
    try:
        response = await create_static(static)
        return {"Result": response}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.get("/{name}", response_model=Static)
async def get_static_content(title: str):
    response = await get_statc(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Content: {title} not found!")


@router.put("/{id}", response_model=Static)
async def update_static_content(static_id: str, static: Static):
    response = await update_static(static, static_id)

    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Content: {static} not found!")


@router.delete("/{id}", response_model=Static)
async def delete_static_content(static_id: str):
    response = await delete_static(static_id)

    if response:
        return response
    raise HTTPException(status_code=404, detail=f"Content: {static_id} not found!")
