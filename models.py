from sqlalchemy import Column, Integer, String, Text, Boolean
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'User(id={self.id}, username={self.username})'
    

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False, index=True)
    description = Column(Text, default='')
    status = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f'Task(id={self.id}, name={self.name})'
    
