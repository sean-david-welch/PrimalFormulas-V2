import uvicorn

from boto3 import client as botoclient
from utils.config import settings

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.about import router as about_router
from routes.static import router as static_router
from routes.auth import router as auth_router


app = FastAPI(
    root_path="/",
    debug=True,
    title="Primal Formulas API",
)

origins = ["http://localhost:4200", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = botoclient(
    "s3",
    aws_access_key_id=settings["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=settings["AWS_SECRET_ACCESS_KEY"],
)
BUCKET_NAME = "primalformulas-bucket"


@app.get("/", response_model=None)
def root() -> RedirectResponse | JSONResponse:
    try:
        return RedirectResponse(url="docs")
    except Exception as error:
        return JSONResponse(
            content={"Error": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


app.include_router(about_router, prefix="/api/about")
app.include_router(static_router, prefix="/api/static")
app.include_router(auth_router, prefix="/api/auth")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
