import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.auth import initialize_firebase

from routes.about_routes import router as about_router
from routes.auth_routes import router as auth_router
from routes.assets_routes import router as assets_router
from routes.payments_routes import router as payments_router
from routes.product_routes import router as products_router

logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Primal Formulas API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(assets_router, prefix="/api/assets", tags=["Assets"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])


if __name__ == "__main__":
    initialize_firebase()
