from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:4200", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_starup():
    pass


@app.get("/", response_model=None)
def root() -> RedirectResponse | JSONResponse:
    try:
        return RedirectResponse(url="docs")
    except Exception as error:
        return JSONResponse(
            content={"Error": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
