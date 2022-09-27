from fastapi import FastAPI
from core import models
from core.database import engine
from endpoints import users, admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
