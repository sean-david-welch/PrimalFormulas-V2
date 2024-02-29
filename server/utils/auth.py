import json
import logging
import firebase_admin

from utils.config import settings
from firebase_admin import credentials, auth

logger = logging.getLogger()


def initialize_firebase():
    service_account_info = json.loads(settings["SERVICE_ACCOUNT_STRING"])
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)


async def verify_token(cookie: str) -> tuple[dict, Exception]:
    try:
        decoded_token = auth.verify_session_cookie(cookie, check_revoked=True)
        is_admin = decoded_token.get("claims", {}).get("admin", False)

        auth_credentials = {"deconded_token": decoded_token, "is_admin": is_admin}

        return auth_credentials
    except Exception as error:
        logger.error(f"Error verifying cookie: {error}")
        return error
