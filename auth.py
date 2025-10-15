import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str):
    password = f"{plain_password}:{config.SECRET_KEY}"
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    password = f"{password}:{config.SECRET_KEY}"
    return pwd_context.verify(password, hashed_password)

def generate_token(data: dict):
    to_encode = data.copy()
    encoded = jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")
    return encoded

def verify_token(token: str):
    try:
        data = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
        return data
    except:
        raise HTTPException(status_code=400, detail="invalid token")
