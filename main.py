from fastapi import FastAPI
from db import engine, Base
from models import *
from routers import router

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(router)
