from passlib.context import CryptContext
from config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str):
    password = f"{plain_password}:{config.SECRET_KEY}"
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    password = f"{password}:{config.SECRET_KEY}"
    return pwd_context.verify(password, hashed_password)
