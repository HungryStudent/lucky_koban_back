from fastapi import APIRouter, Depends, Cookie, HTTPException
from typing import List

import jwt
from sqlalchemy.orm import Session

from configs import salt

from core.database import SessionLocal
from core import crud, models
from core import schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_info_token(token):
    try:
        user_data = jwt.decode(token, salt, algorithms=["HS256"])
    except:
        raise HTTPException(400, "invalid token")
    return user_data["user_id"]


@router.get('/get_me', response_model=schemas.UserInfo)
async def get_cases(db: Session = Depends(get_db), token: str = Cookie()):
    user_id = get_info_token(token)

    return crud.get_user(db, user_id)


@router.post('/reg', response_model=schemas.AuthResponse, description="Registration")
async def reg_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.add_user(db, user_data)


@router.post('/sign', response_model=schemas.AuthResponse)
async def sign_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.sign_user(db, user_data)
