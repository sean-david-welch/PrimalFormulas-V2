from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from models.models import Product, User
from utils.security import get_current_user
from database.products import (
    get_product,
    get_all_products,
    create_product,
    update_product,
    delete_product,
)

router = APIRouter()


@router.get("", response_model=list[Product])
async def get_products_content():
    try:
        response = await get_all_products()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.get("/{id}", response_model=Product)
async def get_product_detail(product_id: str):
    try:
        response = await get_product(product_id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("", response_model=Product)
async def post_product(product: Product, user: User = Depends(get_current_user)):
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await create_product(product)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}", response_model=Product)
async def put_product(
    product: Product, product_id: str, user: User = Depends(get_current_user)
):
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await update_product(product, product_id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}", response_model=None)
async def delete_product_content(
    product_id: str, user: User = Depends(get_current_user)
):
    if user.role != "superuser":
        raise HTTPException(status_code=403, detail="Permission denied")

    try:
        response = await delete_product(product_id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
