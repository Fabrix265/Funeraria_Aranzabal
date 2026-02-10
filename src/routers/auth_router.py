from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

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

"""
"@app.post("/token", tags=["seguridad"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Usuario no encontrado o contraseña incorrecta")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return { "access_token": token }

@app.get("/users/profile", tags=["seguridad"])
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user
"""