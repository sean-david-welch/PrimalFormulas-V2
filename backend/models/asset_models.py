from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Asset(BaseModel):
    id: UUID
    title: str
    media: str
    created: Optional[datetime] = None


class AssetMutation(BaseModel):
    title: str
    media: str
