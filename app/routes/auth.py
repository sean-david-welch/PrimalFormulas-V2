from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from models.models import User
from utils.types import Token
from utils.config import settings
from utils.security import (
    get_current_user,
    authenticate_user,
    create_access_token,
    is_authenticated,
)
from database.users import get_all_users

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user: User = await authenticate_user(form_data.username, form_data.password)

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    access_token_expires = timedelta(
        minutes=int(settings["ACCESS_TOKEN_EXPIRE_MINUTES"])
    )
    access_token = create_access_token({"sub": user.username}, access_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="None",
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.get("/current-user", response_model=User)
async def return_current_user(current_user: User = Depends(get_current_user)):
    return await current_user


@router.get("/is-authenticated")
async def get_authentication_status(authenticated: bool = Depends(is_authenticated)):
    return {"is_authenticated": authenticated}


@router.get("/users", response_model=List[User])
async def get_users(authenticated: bool = Depends(is_authenticated)):
    try:
        response = await get_all_users()

    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
