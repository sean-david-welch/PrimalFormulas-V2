from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from models.asset_models import Asset
from utils.aws import generate_presigned_url

import database.assets_database as database

router = APIRouter()


@router.get("/", response_model=list[Asset])
async def get_assets():
    try:
        response = await database.get_assets()

        if response is not None:
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while getting the content",
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.get("/{title}", response_model=Asset)
async def get_asset_by_title(title: str):
    try:
        response = await database.get_asset_by_title(title)

        if response is not None:
            return response
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while getting the content",
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.post("/", response_model=dict)
async def create_asset(asset: Asset):
    try:
        media_url, presigned_url = generate_presigned_url("assets", asset.media)
        asset.media = media_url

        response = await database.create_asset(asset)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the content",
            )

        return {"asset": asset, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.put("/{id}", response_model=dict)
async def update_asset(id: str, asset: Asset):
    try:
        if asset.image != "" and asset.image.lower() != "null":
            image_url, presigned_url = generate_presigned_url("products", asset.image)
            asset.image = image_url

        response = await database.update_asset(id, asset)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the content",
            )

        return {"asset": asset, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.delete("/{id}", response_model=dict)
async def delete_asset(id: str):
    try:
        response = await database.delete_asset(id)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the content.",
            )

        return {"message": f"content deleted successfully: {response}"}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
