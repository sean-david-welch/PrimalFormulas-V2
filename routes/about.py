from fastapi import APIRouter

router = APIRouter()


@router.get("/about")
def get_about_content():
    response = {"Message": "About router"}
    return response
