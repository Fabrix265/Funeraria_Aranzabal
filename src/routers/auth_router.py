from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from src.core.security import encode_token, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()


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


@auth_router.post("/token", tags=["seguridad"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Usuario no encontrado o contraseña incorrecta")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return { "access_token": token }

@auth_router.get("/users/profile", tags=["seguridad"])
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user
