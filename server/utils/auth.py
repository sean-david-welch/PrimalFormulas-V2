import logging
import firebase_admin as firebase  # type: ignore
from firebase_admin import credentials, auth  # type: ignore

from utils.config import settings
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

logger = logging.getLogger()


def initialize_firebase() -> None:
    service_account_info = settings["SERVICE_ACCOUNT_STRING"]
    cred: credentials.Certificate = firebase.credentials.Certificate(
        service_account_info
    )
    firebase.initialize_app(cred, {}, "primal-formulas")  # type: ignore


async def verify_token(request: Request) -> JSONResponse:
    cookie = request.cookies.get("access_token")

    if not cookie:
        raise HTTPException(status_code=401, detail="cookie is not present")
    try:
        decoded_token: str = firebase.auth.verify_session_cookie(  # type: ignore
            cookie, check_revoked=True
        )

        return JSONResponse({"decoded_token": decoded_token})
    except Exception as error:
        logger.error(f"Error verifying cookie: {error}")
        raise HTTPException(status_code=401, detail="Unauthorized, Invalid Token")


async def verify_token_admin(request: Request) -> JSONResponse:
    cookie = request.cookies.get("access_token")

    if not cookie:
        raise HTTPException(status_code=401, detail="cookie is not present")

    try:
        decoded_token = auth.verify_session_cookie(cookie, check_revoked=True)  # type: ignore
        is_admin = decoded_token.get("claims", {}).get("admin", False)  # type: ignore

        if not is_admin:
            raise HTTPException(
                status_code=403, detail="Forbidden, requires admin privileges"
            )

        return JSONResponse({"deconded_token": decoded_token, "is_admin": is_admin})
    except Exception as error:
        logger.error(f"Error verifying cookie: {error}")
        raise HTTPException(status_code=401, detail="Unauthorized, Invalid Token")
