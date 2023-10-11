import logging
from fastapi.logger import logger as app_logger

from boto3 import client as botoclient
from utils.config import settings

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.about import router as about_router
from routes.static import router as static_router
from routes.auth import router as auth_router
from routes.register import router as register_router
from routes.products import router as product_router
from routes.payments import router as payments_router

logging.basicConfig(level=logging.INFO)


app = FastAPI(
    root_path="/",
    debug=True,
    title="Primal Formulas API",
)

origins = ["*"]

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


@app.get("/", response_model=None, tags=["Default"])
def root() -> RedirectResponse | JSONResponse:
    try:
        app_logger.info("Redirecting to docs")
        return RedirectResponse(url="docs")
    except Exception as error:
        app_logger.exception(f"An error occurred: {error}")
        return JSONResponse(
            content={"Error": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


app.include_router(about_router, prefix="/api/about", tags=["About"])
app.include_router(static_router, prefix="/api/static", tags=["Static"])

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(register_router, prefix="/api/register", tags=["Registration"])

app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
