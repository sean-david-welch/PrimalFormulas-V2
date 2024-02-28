from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from models.models import Asset

import database.assets as database

router = APIRouter()


@router.get("/", response_model=list[Asset])
async def get_assets():
    try:
        response = await database.get_assets()
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.get("/{title}", response_model=Asset)
async def get_asset_by_title(title: str):
    try:
        response = await database.get_asset_by_title(title)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.post("/", response_model=bool)
async def create_asset(asset: Asset):
    try:
        response = await database.create_asset(asset)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.put("/{id}", response_model=bool)
async def update_asset(id: str, asset: Asset):
    try:
        response = await database.update_asset(id, asset)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response


@router.delete("/{id}", response_model=bool)
async def delete_asset(id: str, asset: Asset):
    try:
        response = await database.delete_asset(id, asset)
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code

    return response
