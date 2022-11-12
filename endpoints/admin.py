import os.path

from fastapi import APIRouter, Depends, Cookie, HTTPException, File, UploadFile, Form
from fastapi import Response
from typing import List

from sqlalchemy.orm import Session

from core.database import SessionLocal
from core import crud
from core import schemas

from configs import admin_info, true_admin_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_admin_token(token):
    if token != true_admin_token:
        raise HTTPException(401, "invalid token")


@router.post('/login', response_model=schemas.BaseResponse, tags=["Auth Methods"])
async def login_admin(response: Response, user_data: schemas.UserCreate):
    if user_data == admin_info:
        response.set_cookie(key="admin_token", value=true_admin_token)
        return schemas.BaseResponse(status=True, msg="login is sucessful")
    raise HTTPException(400, "invalid data")


@router.post('/cases/add', status_code=201)
async def add_case(admin_token: str = Cookie(), photo: UploadFile = File(...), name=Form(...), price=Form(...),
                   db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    if os.path.splitext(photo.filename)[1] != ".png":
        raise HTTPException(415, "is not png file")
    crud.add_case(name, price, photo.file.read(), db)
    return {"message": f"{name} is created"}
