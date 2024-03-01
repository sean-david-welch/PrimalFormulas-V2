import stripe

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


from utils.config import settings
from models.data_models import PaymentData

router = APIRouter()

stripe.api_key = settings["STRIPE_SECRET_KEY"]


@router.post("/create-checkout-session")
async def create_checkout_session(data: PaymentData) -> JSONResponse:
    frontend_url = "http://localhost:5173/"

    if not data.cart:
        raise HTTPException(400, {"error": "cart is empty"})

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
        # customer = create_customer(data.customer)

        session = stripe.checkout.Session.create(
            ui_mode="embedded",
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=frontend_url + "checkout/success",
            cancel_url=frontend_url + "checkout/canceled",
            automatic_tax={"enabled": True},
        )

        return JSONResponse({"client_secret": session.client_secret}, status_code=200)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=400)
