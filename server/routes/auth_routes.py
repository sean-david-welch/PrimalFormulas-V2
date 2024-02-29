from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.post("/login", response_model=dict)
async def login():
    pass


@router.post("/logout", response_model=dict)
async def logout():
    pass


@router.post("/register", response_model=dict)
async def register():
    pass


@router.post("/users", response_model=dict)
async def users():
    pass
