from stripe import Webhook, PaymentIntent, checkout
from stripe import Customer as StripeCustomer
from stripe.error import (
    CardError,
    StripeError,
    StripeError,
    RateLimitError,
    IdempotencyError,
    APIConnectionError,
    AuthenticationError,
    InvalidRequestError,
    StripeErrorWithParamCode,
)

from utils.types import PaymentData, Customer


def create_customer(data: PaymentData):
    existing_customers = Customer.list(email=data.customer.email).get("data")
    if existing_customers:
        return existing_customers[0]

    return Customer.create(
        name=data.customer.name,
        address={
            "line1": data.customer.address.line1,
            "city": data.customer.address.city,
            "state": data.customer.address.state,
            "postal_code": data.customer.address.postal_code,
            "country": data.customer.address.country,
        },
        email=data.customer.email,
        shipping={
            "name": data.customer.name,
            "address": {
                "line1": data.customer.address.line1,
                "city": data.customer.address.city,
                "state": data.customer.address.state,
                "postal_code": data.customer.address.postal_code,
                "country": data.customer.address.country,
            },
        },
    )


def handle_stripe_error(error: StripeError):
    error_types = {
        CardError: "A card error occurred",
        RateLimitError: "Too many requests made to the API too quickly",
        InvalidRequestError: "Invalid parameters were supplied to Stripe's API",
        AuthenticationError: "Authentication with Stripe's API failed",
        APIConnectionError: "Network communication with Stripe failed",
        StripeError: "Display a very generic error to the user, and maybe send yourself an email",
        IdempotencyError: "Idempotency errors occur when an Idempotency-Key is re-used on a request that does not match the first request's API endpoint and parameters",
        StripeErrorWithParamCode: "Stripe error with param code",
    }
    error_type = type(error)
    error_message = error_types.get(error_type, "An unexpected error occurred")
    print(error_message, error)
