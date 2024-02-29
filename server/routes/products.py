from fastapi import APIRouter
from models.models import Product
from utils.aws import generate_presigned_url
from fastapi.exceptions import HTTPException

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


@router.post("/", response_model=dict)
async def create_product(product: Product):
    try:
        image_url, presigned_url = generate_presigned_url("products", product.image)

        product.image = image_url

        response = await database.create_product(product)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return {"product": product, "presigned_url": presigned_url}


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
