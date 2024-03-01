from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from models.asset_models import Asset
from utils.aws import generate_presigned_url
from utils.auth import verify_token_admin

import database.assets_database as database

router = APIRouter()


@router.get("/", response_model=Asset)
async def get_assets():
    try:
        assets = await database.get_assets()

        if assets is not None:
            return JSONResponse(status_code=200, content={"assets": assets})
        else:
            raise HTTPException(
                200, {"error": "An error occurred while getting the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.get("/{title}", response_model=Asset)
async def get_asset_by_title(title: str):
    try:
        asset = await database.get_asset_by_title(title)

        if asset is not None:
            return JSONResponse(status_code=200, content={"asset": asset})
        else:
            raise HTTPException(
                200, {"error": "An error occurred while getting the content"}
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.post("/", response_model=dict)
async def create_asset(asset: Asset, request: Request):
    await verify_token_admin(request)

    try:
        media_url, presigned_url = generate_presigned_url("assets", asset.media)
        asset.media = media_url

        response = await database.create_asset(asset)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"asset": asset, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500,
                {"error": "An error occurred while creating the content"},
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.put("/{id}", response_model=dict)
async def update_asset(id: str, asset: Asset, request: Request):
    await verify_token_admin(request)

    try:
        if asset.image != "" and asset.image.lower() != "null":
            image_url, presigned_url = generate_presigned_url("products", asset.image)
            asset.image = image_url

        response = await database.update_asset(id, asset)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"asset": asset, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500,
                {"error": "An error occurred while updating the content"},
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)


@router.delete("/{id}", response_model=dict)
async def delete_asset(id: str, request: Request):
    await verify_token_admin(request)

    try:
        response = await database.delete_asset(id)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"message": f"content deleted successfully: {response}"},
            )
        else:
            raise HTTPException(
                500,
                {"error": "An error occurred while deleting the content"},
            )
    except HTTPException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
