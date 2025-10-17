from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from auth import hash_password, verify_password, generate_token
from db import LocalSession
from models import User, Task
from schemas import UserOut, TaskCreate
from deps import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.get('/')
def home():
    return {'message': 'hello world'}


@router.post('/users', response_model=UserOut)
def regsiter(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists.")
    
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post('/users/login')
def login(
    username: str = Form(min_length=5, max_length=128),
    password: str = Form(min_length=8),
    session = Depends(get_db)
):
    existing_user = session.query(User).filter_by(username=username).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password.")
    
    data = {
        "sub": existing_user.id,
    }
    token = generate_token(data)
    
    return {'token': 654645}


@router.post('/tasks')
def add_task(
    task: TaskCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    # session = Depends(get_db)
):
    print(token)
    print(task)

    # user = session.query(User).filter_by(id=task.user_id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    # # check name
    # existing_task = session.query(Task).filter(Task.user_id==task.user_id, Task.name==task.name).first()
    # if existing_task:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="task already exists.")
    
    # task = Task(name=task.name, description=task.description, user_id=task.user_id)

    # session.add(task)
    # session.commit()
    # session.refresh(task)

    # # return task
    