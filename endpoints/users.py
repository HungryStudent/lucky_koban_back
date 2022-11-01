from fastapi import APIRouter, Depends, Cookie, HTTPException, Body
from fastapi import Response
from typing import List

import email_validate
import jwt
from jwt import DecodeError
from sqlalchemy.orm import Session

from configs import salt

from core.database import SessionLocal
from core import crud, models, schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_info_token(token: str = Cookie()):
    try:
        user_data = jwt.decode(token, salt, algorithms=["HS256"])
    except DecodeError:
        raise HTTPException(401, "invalid token")
    return user_data["user_id"]


@router.get('/get_me', response_model=schemas.UserInfo)
async def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(get_info_token)):
    return crud.get_user(db, user_id)


@router.post('/reg', response_model=schemas.BaseResponse, description="Registration", tags=["Auth Methods"])
async def reg_user(response: Response, user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if not email_validate.validate(user_data.email, check_smtp=False):
        raise HTTPException(400, "invalid email")
    token = crud.add_confirm_user(db, user_data)
    response.set_cookie(key="token", value=token)
    return schemas.BaseResponse(status=True, msg="reg is sucessful")


@router.post('/login', response_model=schemas.BaseResponse, tags=["Auth Methods"])
async def sign_user(response: Response, user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    token = crud.sign_user(db, user_data)
    response.set_cookie(key="token", value=token)
    return schemas.BaseResponse(status=True, msg="login is sucessful")


@router.post('/send_email_code', tags=["Auth Methods"])
async def send_email_code(email: schemas.Email, db: Session = Depends(get_db)):
    return HTTPException(204, "in development")
    # code = crud.gen_code(db, user_id)
