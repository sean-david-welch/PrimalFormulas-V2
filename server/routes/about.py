from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from models.models import About

import database.about as database

router = APIRouter()


@router.get("/", response_model=list[About])
async def get_abouts():
    try:
        response = await database.get_abouts()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("/", response_model=bool)
async def create_about(about: About):
    try:
        response = await database.create_about(about)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}", response_model=bool)
async def update_about(id: str, about: About):
    try:
        response = await database.update_about(id, about)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}", response_model=bool)
async def delete_about(id: str, about: About):
    try:
        response = await database.delete_about(id, about)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
