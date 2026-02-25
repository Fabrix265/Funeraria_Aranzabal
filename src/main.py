from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.core.lifespan import lifespan

from src.routers.auth_router import auth_router
from src.utils.http_error_handler import http_error_handler

app = FastAPI(
    title="Inventario Funeraria Aranzabal API",
    version="1.0",
    lifespan=lifespan
)

app.middleware("http")(http_error_handler)

@app.get("/", tags=["Home"])
def home():
    return JSONResponse(content={"message": "Funcionando"})

app.include_router(prefix="/auth", router=auth_router)