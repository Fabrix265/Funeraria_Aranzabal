from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from src.core.lifespan import lifespan
from src.routers.auth_router import auth_router
from src.utils.http_error_handler import http_error_handler
from src.routers.user_router import user_router

app = FastAPI(
    title="Inventario Funeraria Aranzabal API",
    version="1.0",
    lifespan=lifespan
)

app.middleware("http")(http_error_handler)

@app.get("/", tags=["Home"])
def home():
    return JSONResponse(content={"message": "Funcionando"})

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

app.include_router(user_router, prefix="/users", tags=["Usuarios"])
