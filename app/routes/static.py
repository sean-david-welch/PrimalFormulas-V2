from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Body

from models.models import Static
from database.database import create_static

router = APIRouter()


@router.post("/static")
async def post_static(static: Static = Body(...)):
    try:
        response = await create_static(static)
        return {"Result": response}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
