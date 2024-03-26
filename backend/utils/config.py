import os
from typing import Dict
from dotenv import load_dotenv


load_dotenv()

settings: Dict[str, str] = {
    "DATABASE_URL": os.getenv("DATABASE_URL", ""),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", ""),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    "STRIPE_SECRET_KEY": os.getenv("STRIPE_SECRET_KEY", ""),
    "STRIPE_SECRET_KEY_TEST": os.getenv("STRIPE_SECRET_KEY_TEST", ""),
    "SERVICE_ACCOUNT_STRING": os.getenv("SERVICE_ACCOUNT_STRING", ""),
}
