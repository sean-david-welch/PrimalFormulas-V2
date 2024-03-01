import logging
import stripe

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse


from utils.config import settings
from models.data_models import PaymentData

router = APIRouter()

logger = logging.getLogger()

stripe.api_key = settings["STRIPE_SECRET_KEY"]


@router.post("/create-checkout-session")
async def create_checkout_session(data: PaymentData, ui_mode: str) -> JSONResponse:
    frontend_url = "http://localhost:5173/"

    if not data.cart:
        raise HTTPException(400, {"error": "cart is empty"})

    line_items = [
        {
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
        for item in data.cart
    ]

    try:
        session = stripe.checkout.Session.create(
            ui_mode=ui_mode,
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=frontend_url + "checkout/success",
            cancel_url=frontend_url + "checkout/canceled",
            automatic_tax={"enabled": True},
        )

        if ui_mode == "embedded":
            logger.info(f"client secret: {session.client_secret}")
            return JSONResponse(
                {"client_secret": session.client_secret}, status_code=200
            )
        elif ui_mode == "hosted":
            logger.info(f"checkout url: {session.url}")
            return RedirectResponse(url=f"{frontend_url}/{session.url}")

    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=400)
