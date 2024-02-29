import json

from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0, le=9999.99)
    image: Optional[str] = None
    created: Optional[datetime] = None


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)  # convert UUID to str
        elif isinstance(obj, datetime):
            return obj.isoformat()  # convert datetime to ISO format string
        return super().default(obj)


class ProductMutation(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0, le=9999.99)
    image: Optional[str] = None
