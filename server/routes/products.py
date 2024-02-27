from fastapi import APIRouter
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


@router.get("/{id}", response_model=Product)
async def get_product_by_id(id: str):
    try:
        response = await database.get_product_by_id(id)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("/", response_model=bool)
async def create_product(product: Product):
    try:
        response = await database.create_product(product)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}", response_model=bool)
async def update_product(id: str, product: Product):
    try:
        response = await database.update_product(id, product)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}", response_model=bool)
async def delete_product(id: str, product: Product):
    try:
        response = await database.delete_product(id, product)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
