from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    # add extra fields: first_name(required), last_name, birth_date, phone, email

    # role: admin, user(default), oxirida

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username})'
    

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False, index=True)
    description = Column(Text, default='')
    status = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # add extra fields: category, priority(1-5)

    def __repr__(self) -> str:
        return f'Task(id={self.id}, name={self.name})'
    