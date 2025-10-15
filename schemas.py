from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: int
    username: str
    hashed_password: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    name: str = Field(max_length=128)
    description: str | None = Field(None)
    

class TaskOut(TaskCreate):
    id: int
    user_id: int
    