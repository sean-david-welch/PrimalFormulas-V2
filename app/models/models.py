from uuid import uuid4
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

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


class Token(BaseModel):
    access_token: str
    token_type: str


class Address(BaseModel):
    line1: str = Field(default="Address Line 1")
    city: str = Field(default="City")
    state: str = Field(default="State")
    postal_code: str = Field(default="Postal Code")
    country: str = Field(default="Country")


class Customer(BaseModel):
    id: Optional[str] = Field(default="string")
    name: str = Field(default="Customer Name")
    address: Address = Field(default=Address())
    email: Optional[EmailStr] = Field(default="johndoe@example.come")


class CartItem(BaseModel):
    price: float = Field(default=1.0)
    quantity: int = Field(default=1)


class PaymentIntent(BaseModel):
    cart_items: List[CartItem] = Field(default=[CartItem()])
    customer: Customer = Field(default=Customer())
    receipt_email: Optional[EmailStr] = Field(default="guest@primalformulas.ie")


class Order(BaseModel):
    id: Optional[str] = Field(default="string")
    customer: Customer = Field(default=Customer())
    cart_items: List[CartItem] = Field(default=[CartItem()])
    receipt_email: Optional[EmailStr] = Field(default="guest@primalformulas.ie")
