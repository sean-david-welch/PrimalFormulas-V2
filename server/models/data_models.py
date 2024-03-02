from typing import Optional
from pydantic import BaseModel, Field


class CartItem(BaseModel):
    name: str = Field(default="item")
    description: str = Field(default="item description")
    image: str = Field(default="https://via.placeholder.com/150")
    price: float = Field(default=1.0)
    quantity: int = Field(default=1)


class PaymentData(BaseModel):
    cart: list[CartItem] = Field(default=[CartItem()])


class User(BaseModel):
    email: str
    password: str
    role: Optional[str] = Field("user" or "admin")
