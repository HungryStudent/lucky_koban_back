from fastapi import APIRouter, Depends, Cookie, HTTPException
from fastapi import Response
from typing import List

import email_validate
import jwt
from jwt import DecodeError
from sqlalchemy.orm import Session

from configs import salt

from core.database import SessionLocal
from core import crud, schemas

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


@router.get('/get_me', response_model=schemas.UserInfo, tags=["User Methods "])
async def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(get_info_token)):
    return crud.get_user(db, user_id)


@router.post('/reg', response_model=schemas.BaseResponse, description="Registration", tags=["Auth Methods"])
async def reg_user(response: Response, user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    if not email_validate.validate(user_data.email, check_smtp=False):
        raise HTTPException(400, "invalid email")
    if crud.check_email(db, user_data.email):
        raise HTTPException(400, "this email is already taken")
    token = crud.add_user(db, user_data)
    response.set_cookie(key="token", value=token, httponly=True)
    return schemas.BaseResponse(status=True, msg="reg is successful")


@router.post('/activate', response_model=schemas.BaseResponse, tags=["Auth Methods"])
async def check_code(code: schemas.Code, db: Session = Depends(get_db), user_id: str = Depends(get_info_token)):
    crud.check_code(code.code, user_id, db)
    return schemas.BaseResponse(status=True, msg="account is activate")


@router.get('/send_code', response_model=schemas.BaseResponse, tags=["Auth Methods"])
async def send_code(db: Session = Depends(get_db), user_id: str = Depends(get_info_token)):
    crud.change_code(user_id, db)
    return schemas.BaseResponse(status=True, msg="code has been sent")


@router.post('/login', response_model=schemas.BaseResponse, tags=["Auth Methods"])
async def sign_user(response: Response, user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    token = crud.sign_user(db, user_data)
    response.set_cookie(key="token", value=token)
    return schemas.BaseResponse(status=True, msg="login is sucessful")


