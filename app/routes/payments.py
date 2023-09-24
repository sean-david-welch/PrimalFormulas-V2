from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from models.models import User
from utils.security import get_current_user

from stripe import api_key
from stripe import checkout
from stripe.error import StripeError

from utils.config import settings
from utils.types import PaymentData
from utils.stripe import handle_stripe_error, create_customer

router = APIRouter()


@router.post("/create-checkout-session")
async def create_checkout_session(data: PaymentData) -> JSONResponse:
    api_key = settings["STRIPE_SECRET_KEY"]
    frontend_url = "https://www.primalformulas.ie/"

    if not data.cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )

    line_items = []
    for item in data.cart:
        line_item = {
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": item["name"],
                    "description": item["description"],
                    "images": [item["image"]],
                },
                "unit_amount": int(item["price"] * 100),
                "tax_behavior": "inclusive",
            },
            "quantity": item.get("quantity", 1),
        }
        line_items.append(line_item)

    try:
        customer = create_customer(data.customer)

        checkout_session = checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=frontend_url + "checkout/success",
            cancel_url=frontend_url + "checkout/canceled",
            automatic_tax={"enabled": True},
        )

    except StripeError as error:
        handle_stripe_error(error)
        return JSONResponse(
            content={"error": str(error)}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse({"id": checkout_session.id})
