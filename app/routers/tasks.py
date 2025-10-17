from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.db.models import User, Task
from app.schemas.task import TaskCreate, TaskOut
from app.dependencies import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post('/', response_model=TaskOut)
def add_task(
    task: TaskCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db)]
):
    data = verify_token(token)
    
    sub = data['sub']

    user = session.query(User).filter_by(username=sub).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")

    existing_task = session.query(Task).filter(Task.user_id==user.id, Task.name==task.name).first()
    if existing_task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="task already exists.")
    
    task = Task(name=task.name, description=task.description, user_id=user.id)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch('/{task_id}', response_model=TaskOut)
def update_status(
    task_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db)]
):
    data = verify_token(token)
    user = session.query(User).filter_by(username=data['sub']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found.")
    
    task = session.query(Task).filter(Task.id==task_id, Task.user_id==user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="task not found.")
    
    task.status = not task.status
    session.add(task)
    session.commit()

    return task
