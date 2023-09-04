from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

from utils.config import settings


##### About Content #####
class AboutContent(BaseModel):
    id: Optional[str] = Field(default=uuid4(), example="null")
    title: str
    description: str
    image: str = Field(default=f"{settings['BASE_URL']}/images/default.jpg")
