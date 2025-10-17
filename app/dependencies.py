from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.db.models import User
from app.db.session import LocalSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_db() -> Session:
    return LocalSession()

def get_current_user(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    data = verify_token(token)
    user = session.query(User).filter_by(username=data['sub']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")
    
    return user
