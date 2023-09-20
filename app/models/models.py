from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from utils.config import settings


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
    name: str = Field(default="User Name")
    email: Optional[EmailStr] = Field(default="johndoe@example.com")
    password_hash: str = Field(default="password")
    full_name: Optional[str] = Field(default="John Doe")
    disabled: Optional[bool] = Field(default=False)
    is_superuser: Optional[bool] = Field(default=False)
