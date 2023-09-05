from utils.config import settings
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import (
    DuplicateKeyError,
    OperationFailure,
    ServerSelectionTimeoutError,
)

from models.models import Static, AboutContent, Product, User
from .utils import database_insert_one

client = AsyncIOMotorClient(settings["MONGO_URI"])

database = client.PrimalFormulas
collections = {
    "static": database.Static,
    "users": database.Users,
    "about": database.About,
    "products": database.Products,
    "orders": database.Orders,
}


async def create_static(static: Static):
    try:
        result = await database_insert_one(
            collection=collections["static"], data=static
        )
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return result


async def get_statc(title: str) -> Static:
    static_data = await collections["static"].find_one({"title": title})

    if not static_data:
        raise HTTPException(status_code=404, detail="Model data not found")

    try:
        return Static(**static_data)
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))
