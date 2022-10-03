from fastapi import FastAPI
from core import models
from core.database import engine
from endpoints import users, admin, items

models.Base.metadata.create_all(bind=engine)
app = FastAPI(root_path="api", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.include_router(users.router, prefix="/user")
app.include_router(items.router, prefix="/api/items")
