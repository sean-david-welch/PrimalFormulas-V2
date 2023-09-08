import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.about import router as about_router

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


@app.get("/", response_model=None)
def root() -> RedirectResponse | JSONResponse:
    try:
        return RedirectResponse(url="docs")
    except Exception as error:
        return JSONResponse(
            content={"Error": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
    )

app.include_router(about_router, prefix="/api")
