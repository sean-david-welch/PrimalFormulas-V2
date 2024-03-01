from stripe import Customer as StripeCustomer
from models.data_models import PaymentData, Customer


def create_customer(data: PaymentData):
    existing_customers = Customer.list(email=data.customer.email).get("data")
    if existing_customers:
        return existing_customers[0]

    return StripeCustomer.create(
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
