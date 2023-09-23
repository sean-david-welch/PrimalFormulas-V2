from models.models import Product
from database.database import (
    collections,
    handle_http_error,
    database_find_all,
    database_find_one,
    database_insert_one,
    database_update_one,
    database_delete_one,
)
from fastapi.exceptions import HTTPException

product_collection = collections["products"]


async def get_all_products() -> list[Product]:
    try:
        result = await database_find_all(product_collection)

    except HTTPException as error:
        handle_http_error(error)
    return result


async def get_product(product_id: str) -> Product:
    try:
        result = await database_find_one(product_collection, product_id)

    except HTTPException as error:
        handle_http_error(error)
    return result


async def create_product(product: Product) -> Product:
    try:
        result = await database_insert_one(product_collection, product)

    except HTTPException as error:
        handle_http_error(error)
    return result


async def update_product(product: Product, product_id: str) -> Product:
    try:
        result = await database_update_one(product_id, product, product_collection)

    except HTTPException as error:
        handle_http_error(error)
    return result


async def delete_product(product_id: str) -> None:
    try:
        result = await database_delete_one(product_id, product_collection)

    except HTTPException as error:
        handle_http_error(error)
    return result
