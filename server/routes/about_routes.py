from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from utils.aws import generate_presigned_url
from models.about_models import About, AboutMutation

import database.about_database as database

router = APIRouter()


@router.get("/", response_model=list[About])
async def get_abouts():
    try:
        about = await database.get_abouts()

        if about is not None:
            return JSONResponse(status_code=200, content={"about": about})
        else:
            raise HTTPException(
                200, {"error": "An error occurred while getting the content"}
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.post("/", response_model=dict)
async def create_about(about: AboutMutation):
    try:
        image_url, presigned_url = generate_presigned_url("about", about.image)
        about.image = image_url

        response = await database.create_about(about)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"about": about, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500,
                {"error": "An error occurred while creating the content"},
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.put("/{id}", response_model=dict)
async def update_about(id: str, about: AboutMutation):
    try:
        if about.image != "" and about.image.lower() != "null":
            image_url, presigned_url = generate_presigned_url("about", about.image)
            about.image = image_url

        response = await database.update_about(id, about)

        if response is not None:
            return JSONResponse(
                status_code=200,
                content={"about": about, "presigned_url": presigned_url},
            )
        else:
            raise HTTPException(
                500,
                {"error": "An error occurred while updating the content"},
            )
    except HTTPException as error:
        return {"Error": error.detail}, error.status_code


@router.delete("/{id}", response_model=dict)
async def delete_about(id: str):
    try:
        response = await database.delete_about(id)

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
        return {"Error": error.detail}, error.status_code
