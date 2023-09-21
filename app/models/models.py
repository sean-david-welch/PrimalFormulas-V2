from utils.config import settings

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Role(Enum):
    USER = "user"
    SUPERUSER = "superusr"


class Static(BaseModel):
    id: Optional[str] = Field(default="string")
    title: str = Field(default="Static Title")
    content: str = Field(default=f"{settings['BASE_URL']}/images/default.jpg")


class AboutContent(BaseModel):
    id: Optional[str] = Field(default="string")
    title: str = Field(default="About Title")
    description: str = Field(default="About Description")
    image: str = Field(default=f"{settings['BASE_URL']}/images/default.jpg")


class Product(BaseModel):
    id: Optional[str] = Field(default="string")
    title: str = Field(default="Product Title")
    desription: str = Field(default="Product Description")
    price: float = Field(default=1.0)
    image: str = Field(default=f"{settings['BASE_URL']}/images/default.jpg")


class User(BaseModel):
    id: Optional[str] = Field(default="string")
    username: str = Field(default="username")
    email: Optional[EmailStr] = Field(default="johndoe@example.com")
    password_hash: str = Field(default="password")
    disabled: Optional[bool] = Field(default=False)
    role: Optional[Role] = Field(default=Role.USER)
