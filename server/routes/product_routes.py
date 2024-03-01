from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from utils.aws import generate_presigned_url
from utils.auth import verify_token_admin
from models.products_models import Product, ProductMutation

import database.products_database as database

router = APIRouter()


@router.get("/", response_model=Product)
async def get_products():
    try:
        products = await database.get_products()

        if products is not None:
            return JSONResponse(status_code=200, content={"products": products})
        else:
            raise HTTPException(
                200, {"error": "An error occurred while getting the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get("/{id}", response_model=Product)
async def get_product_by_id(id: str):
    try:
        product = await database.get_product_by_id(id)

        if product is not None:
            return JSONResponse(status_code=200, content={"product": product})
        else:
            raise HTTPException(
                200, {"error": "An error occurred while getting the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("/", response_model=dict)
async def create_product(product: ProductMutation, request: Request):
    await verify_token_admin(request)

    try:
        image_url, presigned_url = generate_presigned_url("products", product.image)
        product.image = image_url

        response = await database.create_product(product)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"product": product, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500, {"error": "An error occurred while creating the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.put("/{id}", response_model=dict)
async def update_product(id: str, product: ProductMutation, request: Request):
    await verify_token_admin(request)

    try:
        if product.image != "" and product.image.lower() != "null":
            image_url, presigned_url = generate_presigned_url("products", product.image)
            product.image = image_url

        response = await database.update_product(id, product)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"product": product, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500, {"error": "An error occurred while updating the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.delete("/{id}", response_model=dict)
async def delete_product(id: str, request: Request):
    await verify_token_admin(request)

    try:
        response = await database.delete_product(id)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"message": f"content deleted successfully: {response}"},
            )
        else:
            raise HTTPException(
                500, {"error": "An error occurred while deleting the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
