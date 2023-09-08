from pydantic import BaseModel
from pymongo.results import InsertOneResult
from fastapi.exceptions import HTTPException
from pymongo.errors import (
    DuplicateKeyError,
    OperationFailure,
    ServerSelectionTimeoutError,
)
from motor.motor_asyncio import AsyncIOMotorCollection


async def database_insert_one(
    collection: AsyncIOMotorCollection, data: BaseModel
) -> InsertOneResult:
    try:
        result = await collection.insert_one(data.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Duplicate key")
    except OperationFailure:
        raise HTTPException(status_code=500, detail="Operation failed")
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="Cannot connect to MongoDB")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Database Insertion Failed")

    return result
