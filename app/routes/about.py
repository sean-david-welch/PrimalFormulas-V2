from fastapi import APIRouter

from database.database import create_static

router = APIRouter()


@router.get("/about")
def get_about_content():
    response = {"Message": "About router"}
    return response
