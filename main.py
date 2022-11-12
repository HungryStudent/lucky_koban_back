from fastapi import FastAPI
from core import models
from core.database import engine
from endpoints import users, admin, items

models.Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/api", redoc_url="/api/redoc", openapi_url="/api/openapi.json")


app.include_router(users.router, prefix="/api/user")
app.include_router(items.router, prefix="/api/items")
app.include_router(admin.router, prefix="/api/admin")
