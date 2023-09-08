from uuid import uuid4
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo.errors import (
    DuplicateKeyError,
    OperationFailure,
    ServerSelectionTimeoutError,
)

from utils.config import settings
from models.models import Static, AboutContent, Product, User

client = AsyncIOMotorClient(settings["MONGO_URI"])

database = client.PrimalFormulas
collections = {
    "static": database.Static,
    "users": database.Users,
    "about": database.About,
    "products": database.Products,
    "orders": database.Orders,
}


def database_handle_errors(error):
    if isinstance(error, DuplicateKeyError):
        raise HTTPException(status_code=409, detail="Duplicate key")
    elif isinstance(error, OperationFailure):
        raise HTTPException(status_code=500, detail="Operation failed")
    elif isinstance(error, ServerSelectionTimeoutError):
        raise HTTPException(status_code=503, detail="Cannot connect to MongoDB")
    else:
        raise HTTPException(status_code=500, detail="Database Operation Failed")


async def database_insert_one(
    collection: AsyncIOMotorCollection, data: BaseModel
) -> InsertOneResult:
    data.id = str(uuid4())

    try:
        result = await collection.insert_one(data.model_dump())
    except Exception as error:
        database_handle_errors(error)

    return result


async def database_update_one(
    model_id: str,
    model_data: BaseModel,
    collection: AsyncIOMotorCollection,
) -> UpdateResult:
    try:
        result = await collection.update_one(
            {"id": model_id}, {"$set": model_data.model_dump(exclude="id")}
        )
    except Exception as error:
        database_handle_errors(error)

    return result


async def database_delete_one(
    model_id: str, collection: AsyncIOMotorCollection
) -> DeleteResult:
    try:
        result = await collection.delete_one({"id": model_id})
    except Exception as error:
        database_handle_errors(error)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return result
