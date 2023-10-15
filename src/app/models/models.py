from typing_extensions import Literal
from utils.config import settings
from models.enums import Role

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


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
    name: str = Field(default="Product Name")
    description: str = Field(default="Product Description")
    price: float = Field(default=1.0)
    image: str = Field(default=f"{settings['BASE_URL']}/images/default.jpg")


class User(BaseModel):
    id: Optional[str] = Field(default="string")
    username: str = Field(default="username")
    email: Optional[EmailStr] = Field(default="johndoe@example.com")
    password: str = Field(default="password")
    disabled: Optional[bool] = Field(default=False)
    role: Optional[Role] = Field(default=Role.USER)

    class Config:
        use_enum_values = True
