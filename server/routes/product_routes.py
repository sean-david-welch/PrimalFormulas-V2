from fastapi import APIRouter, status
from models.products_models import Product, ProductMutation
from utils.aws import generate_presigned_url
from fastapi.exceptions import HTTPException

import database.products_database as database

router = APIRouter()


@router.get("/", response_model=list[Product])
async def get_products():
    try:
        response = await database.get_products()

        if response is not None:
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while getting the content",
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.get("/{id}", response_model=Product)
async def get_product_by_id(id: str):
    try:
        response = await database.get_product_by_id(id)

        if response is not None:
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while getting the content",
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.post("/", response_model=dict)
async def create_product(product: ProductMutation):
    try:
        image_url, presigned_url = generate_presigned_url("products", product.image)
        product.image = image_url

        response = await database.create_product(product)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the content",
            )

        return {"product": product, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.put("/{id}", response_model=dict)
async def update_product(id: str, product: ProductMutation):
    try:
        if product.image != "" or "null":
            image_url, presigned_url = generate_presigned_url("products", product.image)
            product.image = image_url

        response = await database.update_product(id, product)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the content",
            )

        return {"product": product, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.delete("/{id}", response_model=dict)
async def delete_product(id: str):
    try:
        response = await database.delete_product(id)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the content.",
            )

        return {"message": f"content deleted successfully: {response}"}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
