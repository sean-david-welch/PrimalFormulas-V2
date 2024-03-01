from typing import Optional
from pydantic import BaseModel, Field


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
    email: Optional[str] = Field(default="johndoe@example.come")


class CartItem(BaseModel):
    price: float = Field(default=1.0)
    quantity: int = Field(default=1)


class PaymentData(BaseModel):
    cart: list[CartItem] = Field(default=[CartItem()])
    customer: Optional[Customer] = Field(default=Customer())
