from fastapi import FastAPI, Request, Depends, Header, Response
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.exceptions import HTTPException
from jose import jwt
from sqlmodel import SQLModel
from src.config.db import engine

from src.routers.producto_router import producto_router

from src.utils.http_error_handler import http_error_handler

SQLModel.metadata.create_all(engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "user1": {
        "username": "user1",
        "email": "email1",
        "password": "password1"
    },
    "user2": {
        "username": "user2",
        "email": "email2",
        "password": "password2"
    }
}

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "mysecretkey", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, "mysecretkey", algorithms=["HS256"])
    user = users.get(data["username"])
    return user

@app.post("/token", tags=["seguridad"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Usuario no encontrado o contraseña incorrecta")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return { "access_token": token }

@app.get("/users/profile", tags=["seguridad"])
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user

app.middleware("http")(http_error_handler)

app.title = "Inventario Funeraria Aranzabal API"
app.version = "1.0"

@app.get("/", tags=["Home"])
def home(request: Request):
    return (JSONResponse(content={"message": "Funcionando"}, status_code=200))

app.include_router(prefix="/producto", router=producto_router)
