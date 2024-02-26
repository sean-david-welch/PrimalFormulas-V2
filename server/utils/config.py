import os
from dotenv import load_dotenv


load_dotenv()

settings = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY"),
    "STRIPE_SECRET_KEY_TEST": os.getenv("STRIPE_SECRET_KEY_TEST"),
}
