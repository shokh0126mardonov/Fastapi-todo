from fastapi.routing import APIRouter
from fastapi import Form, HTTPException, status
from auth import hash_password, verify_password
from db import LocalSession
from models import User
from schemas import UserOut

router = APIRouter()


@router.get('/')
def home():
    return {'message': 'hello world'}


@router.post('/users', response_model=UserOut)
def regsiter(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
):
    session = LocalSession()
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists.")
    
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get('/users', response_model=UserOut)
def regsiter(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
):
    session = LocalSession()
    existing_user = session.query(User).filter_by(username=username).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password.")
    
    return existing_user
