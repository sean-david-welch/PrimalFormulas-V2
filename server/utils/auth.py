import json
import logging
import firebase_admin

from utils.config import settings
from firebase_admin import credentials, auth
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


logger = logging.getLogger()


def initialize_firebase():
    service_account_info = json.loads(settings["SERVICE_ACCOUNT_STRING"])
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)


async def verify_token(request: Request) -> dict:
    cookie = request.cookies.get("access_token")

    if not cookie:
        raise HTTPException(status_code=401, detail="cookie is not present")
    try:
        decoded_token = auth.verify_session_cookie(cookie, check_revoked=True)

        return JSONResponse({"decoded_token": decoded_token})
    except Exception as error:
        logger.error(f"Error verifying cookie: {error}")
        raise HTTPException(status_code=401, detail="Unauthorized, Invalid Token")


async def verify_token_admin(request: Request) -> dict:
    cookie = request.cookies.get("access_token")

    if not cookie:
        raise HTTPException(status_code=401, detail="cookie is not present")

    try:
        decoded_token = auth.verify_session_cookie(cookie, check_revoked=True)
        is_admin = decoded_token.get("claims", {}).get("admin", False)

        if not is_admin:
            raise HTTPException(
                status_code=403, detail="Forbidden, requires admin privileges"
            )

        return JSONResponse({"deconded_token": decoded_token, "is_admin": is_admin})
    except Exception as error:
        logger.error(f"Error verifying cookie: {error}")
        raise HTTPException(status_code=401, detail="Unauthorized, Invalid Token")
