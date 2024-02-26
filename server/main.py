import logging

from utils.config import settings
from boto3 import client as botoclient

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.about import router as about_router
from routes.auth import router as auth_router
from routes.content import router as content_router
from routes.payments import router as payments_router
from routes.products import router as products_router

logging.basicConfig(level=logging.DEBUG)


app = FastAPI(
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


@app.get("/")
def root() -> RedirectResponse:
    try:
        return RedirectResponse(url="/docs")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.get("/api")
def root_api() -> RedirectResponse:
    logging.info("Root endpoint accessed")
    try:
        return RedirectResponse(url="/docs")
    except Exception as e:
        logging.error(f"Exception in root: {e}")
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


app.include_router(about_router, prefix="/api/about", tags=["About"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(content_router, prefix="/api/content", tags=["Content"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
