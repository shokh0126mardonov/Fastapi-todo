from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import User


def create_user(session: Session, username: str, password: str) -> User:
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

