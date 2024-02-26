from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.models import Product

import database.products as database

router = APIRouter()


@router.get("/", response_model=list[Product])
async def get_products():
    try:
        response = await database.get_products()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
