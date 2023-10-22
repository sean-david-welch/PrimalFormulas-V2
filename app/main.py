import logging

from boto3 import client as botoclient
from utils.config import settings

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
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
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
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


@app.get("/api")
def root() -> RedirectResponse:
    try:
        return RedirectResponse(url="/api/docs")
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


app.include_router(about_router, prefix="/api/about", tags=["About"])
app.include_router(static_router, prefix="/api/static", tags=["Static"])

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(register_router, prefix="/api/register", tags=["Registration"])

app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
