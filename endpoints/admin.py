import os.path
from typing import List

from fastapi import APIRouter, Depends, Cookie, HTTPException, File, UploadFile, Form
from fastapi import Response

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


@router.post('/cases/create', status_code=201)
async def create_case(admin_token: str = Cookie(), photo: UploadFile = File(...), name=Form(...), price=Form(...),
                      db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    if os.path.splitext(photo.filename)[1] not in [".png", ".jpg"]:
        raise HTTPException(415, "is not png/jpg file")
    crud.create_case(name, price, photo.file.read(), db)
    return {"message": f"{name} is created"}


@router.post('/cases/add_games')
async def add_games_to_case(games_data: schemas.GamesToCase, admin_token: str = Cookie(),
                            db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    crud.add_games_to_case(games_data, db)
    return {"message": f"games added to case"}


@router.post('/games/create', status_code=201)
async def create_game(admin_token: str = Cookie(), photo: UploadFile = File(...), name=Form(...),
                      db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    if os.path.splitext(photo.filename)[1] not in [".png", ".jpg"]:
        raise HTTPException(415, "is not png/jpg file")
    crud.create_game(name, photo.file.read(), db)
    return {"message": f"{name} is created"}


@router.post('/games/add_keys', status_code=201)
async def add_keys(keys_data: schemas.Keys, admin_token: str = Cookie(), db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    crud.add_keys(keys_data, db)
    return {"message": f"keys added to game"}
