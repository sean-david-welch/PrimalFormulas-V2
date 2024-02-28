from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0, le=9999999999.99)
    image: Optional[str] = None
    created: Optional[datetime] = None


class StockInformation(BaseModel):
    id: UUID
    product_id: UUID
    sku: Optional[str] = None
    quantity: Optional[int] = None


class About(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    created: Optional[datetime] = None


class Content(BaseModel):
    id: UUID
    title: str
    media: str
    created: Optional[datetime] = None
