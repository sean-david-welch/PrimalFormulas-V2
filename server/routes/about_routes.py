from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from utils.aws import generate_presigned_url
from models.about_models import About, AboutMutation

import database.about_database as database

router = APIRouter()


@router.get("/", response_model=list[About])
async def get_abouts():
    try:
        response = await database.get_abouts()

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
async def create_about(about: AboutMutation):
    try:
        image_url, presigned_url = generate_presigned_url("about", about.image)
        about.image = image_url

        response = await database.create_about(about)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the content",
            )

        return {"about": about, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.put("/{id}", response_model=dict)
async def update_about(id: str, about: AboutMutation):
    try:
        if about.image != "" and about.image.lower() != "null":
            image_url, presigned_url = generate_presigned_url("about", about.image)
            about.image = image_url

        response = await database.update_about(id, about)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the content",
            )

        return {"about": about, "presigned_url": presigned_url}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.delete("/{id}", response_model=dict)
async def delete_about(id: str):
    try:
        response = await database.delete_about(id)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the content.",
            )

        return {"message": f"content deleted successfully: {response}"}
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code
