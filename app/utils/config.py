import os
from dotenv import load_dotenv


load_dotenv(".env")

settings = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "MONGO_URI": os.getenv("MONGO_URI"),
    "STRIPE_SECRET_KEY_TEST": os.getenv("STRIPE_SECRET_KEY_TEST"),
    "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
    "STRIPE_WEBHOOK_ENDPOINT_SECRET": os.getenv("STRIPE_WEBHOOK_ENDPOINT_SECRET"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),
    "BASE_URL": os.getenv("BASE_URL"),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
}

print(settings)
