import uvicorn

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


app = FastAPI(
    root_path="/",
    debug=True,
    title="Primal Formulas API",
)

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
    "https://primalformulas.ie",
    "https://primalformulas.eu",
    "primalformulas-fastapi-dev.eu-west-1.elasticbeanstalk.com",
]

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
        return RedirectResponse(url="docs")
    except Exception as error:
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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
