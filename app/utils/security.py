from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

from utils.config import settings
from models.models import User
from database.users import get_user

SECRET_KEY = settings["SECRET_KEY"]
ALGORITHM = settings["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings["ACCESS_TOKEN_EXPIRE_MINUTES"])

password_context = CryptContext(schemes=["bcrypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(user_password: str, hashed_password: str) -> bool:
    return password_context.verify(user_password, hashed_password)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> User:
    try:
        user = await get_user(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return user

    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(
            status_code=500, detail="Internal server error" + str(error)
        )


async def cookie_oauth2_scheme(request: Request) -> str:
    token = request.cookies.get("access_token")
    if token is None:
        raise credentials_exception
    return token


async def is_authenticated(token: str = Depends(cookie_oauth2_scheme)) -> bool:
    if token is None:
        return False

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        return username is not None

    except JWTError:
        return False


async def get_current_user(token: str = Depends(cookie_oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        expiration: datetime = datetime.fromtimestamp(payload.get("exp"))

        if expiration and datetime.utcnow() > expiration:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    current_user = await get_user(username)
    if current_user is None:
        raise credentials_exception

    return current_user


async def is_superuser(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "superuser":
        raise HTTPException(status_code=403, detail="Permission Denied")
    return current_user
