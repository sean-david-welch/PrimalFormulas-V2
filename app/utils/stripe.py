from stripe import checkout, Customer, Webhook
import stripe.error

from utils.config import settings
from models.models import CartItem

from fastapi.applications import Request, Response


def create_customer(data):
    existing_customers = stripe.Customer.list(email=data.receipt_email).get("data")
    if existing_customers:
        return existing_customers[0]

    return stripe.Customer.create(
        name=data.customer.name,
        address={
            "line1": data.customer.address.line1,
            "line2": data.customer.address.line2,
            "city": data.customer.address.city,
            "state": data.customer.address.state,
            "postal_code": data.customer.address.postal_code,
            "country": data.customer.address.country,
        },
        email=data.receipt_email,
        shipping={
            "name": data.customer.name,
            "address": {
                "line1": data.customer.address.line1,
                "line2": data.customer.address.line2,
                "city": data.customer.address.city,
                "state": data.customer.address.state,
                "postal_code": data.customer.address.postal_code,
                "country": data.customer.address.country,
            },
        },
    )


def handle_stripe_error(error: stripe.error.StripeError):
    error_types = {
        stripe.error.CardError: "A card error occurred",
        stripe.error.RateLimitError: "Too many requests made to the API too quickly",
        stripe.error.InvalidRequestError: "Invalid parameters were supplied to Stripe's API",
        stripe.error.AuthenticationError: "Authentication with Stripe's API failed",
        stripe.error.APIConnectionError: "Network communication with Stripe failed",
        stripe.error.StripeError: "Display a very generic error to the user, and maybe send yourself an email",
        stripe.error.IdempotencyError: "Idempotency errors occur when an Idempotency-Key is re-used on a request that does not match the first request's API endpoint and parameters",
        stripe.error.StripeErrorWithParamCode: "Stripe error with param code",
    }
    error_type = type(error)
    error_message = error_types.get(error_type, "An unexpected error occurred")
    print(error_message, error)
