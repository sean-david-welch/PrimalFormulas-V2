from firebase_admin import auth
from asyncio import to_thread

from fastapi import APIRouter, Request
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException

from models.data_models import User
from utils.auth import verify_token_admin

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
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("/logout", response_model=dict)
async def logout(response: Response):
    try:
        response.delete_cookie("access_token")

        return JSONResponse(
            status_code=200, content={"message": "logged out successfully"}
        )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("/register", response_model=dict)
async def register(user: User, request: Request):
    await verify_token_admin(request)

    try:
        user_record = await to_thread(
            auth.create_user, email=user.email, password=user.password
        )

        custom_claims = {"admin": user.role == "admin"}
        await to_thread(
            auth.set_custom_user_claims,
            uid=user_record.uid,
            custom_claims=custom_claims,
        )

        return {
            "message": "User created successfully",
            "uid": user_record.uid,
            "admin": custom_claims["admin"],
        }

    except auth.AuthError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/users", response_model=dict)
async def get_users(request: Request):
    # await verify_token_admin(request)

    try:
        users = []

        user_records_generator = await to_thread(auth.list_users)
        for user_record in user_records_generator.iterate_all():
            users.append(
                {
                    "uid": user_record.uid,
                    "email": user_record.email,
                    "is_admin": user_record.custom_claims.get("is_admin", False),
                }
            )

        return {"users": users}
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
