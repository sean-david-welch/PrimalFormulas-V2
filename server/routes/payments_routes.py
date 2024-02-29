from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("create-checkout-session")
async def create_checkout_session() -> JSONResponse:
    pass
