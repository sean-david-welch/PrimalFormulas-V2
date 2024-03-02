import logging

from contextlib import asynccontextmanager


from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.auth import initialize_firebase

from routes.about_routes import router as about_router
from routes.auth_routes import router as auth_router
from routes.assets_routes import router as assets_router
from routes.payments_routes import router as payments_router
from routes.product_routes import router as products_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_firebase()

    try:
        yield
    finally:
        pass


app = FastAPI(title="Primal Formulas API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # type: ignore
def root() -> Response:
    try:
        return RedirectResponse(url="/docs")
    except Exception as e:
        logging.error(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/api")  # type: ignore
def root_api() -> Response:
    logging.info("Root endpoint accessed")
    try:
        return RedirectResponse(url="/docs")
    except Exception as e:
        logging.error(f"Exception in root: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


app.include_router(about_router, prefix="/api/about", tags=["About"])
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(assets_router, prefix="/api/assets", tags=["Assets"])
app.include_router(payments_router, prefix="/api/payments", tags=["Payments"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
