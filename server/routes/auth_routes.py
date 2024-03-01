from firebase_admin import auth

from fastapi import APIRouter, Request
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException


router = APIRouter()


@router.post("/login", response_model=dict)
async def login(response: Response, request: Request) -> dict:
    try:
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            raise HTTPException(
                status_code=401, detail="Authorization header not present"
            )

        scheme, token = auth_header.split()

        if scheme != "bearer":
            raise HTTPException(
                status_code=400, detail="Authorization header is incorrect"
            )

        try:
            auth.verify_id_token(token)
            expires_in = 60 * 60 * 24 * 3
            access_token = auth.create_session_cookie(token, expires_in)
        except auth.AuthError as e:
            raise HTTPException(status_code=401, detail=str(e))

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
        )

        return JSONResponse(status_code=200, content={"message": "login successfu"})
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid authorization header format"
        )
    except HTTPException as error:
        raise error


@router.post("/logout", response_model=dict)
async def logout(response: Response):
    try:
        response.delete_cookie("access_token")

        return JSONResponse(
            status_code=200, content={"message": "logged out successfully"}
        )
    except HTTPException as error:
        raise error


@router.post("/register", response_model=dict)
async def register():
    pass


@router.post("/users", response_model=dict)
async def users():
    pass
