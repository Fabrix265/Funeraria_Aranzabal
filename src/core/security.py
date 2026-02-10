from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECURITY_KEY = os.getenv("SECURITY_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def encode_token(payload: dict) -> str:
    return jwt.encode(payload, SECURITY_KEY, algorithm="HS256")

def decode_token(token: str = Depends(oauth2_scheme)) -> dict:
    data = jwt.decode(token, SECURITY_KEY, algorithms=["HS256"])
    return data