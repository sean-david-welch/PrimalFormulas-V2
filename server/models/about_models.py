from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class About(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    image: str = "null"
    created: Optional[datetime] = None


class AboutMutation(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
