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


class ProductMutation(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0, le=9999.99)
    image: Optional[str] = None
