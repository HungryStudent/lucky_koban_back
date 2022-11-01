from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from core import models, schemas

import random
import string
import jwt

import hashlib
from configs import salt


def get_cases(db: Session):
    return db.query(models.Cases).all()

def add_confirm_user(db: Session, user_data: schemas.UserCreate):
    letters = string.ascii_uppercase
    code = ''.join(random.choice(letters) for i in range(5))
    print(code)
def add_user(db: Session, user_data: schemas.UserCreate):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode('utf-8'))
    password_hash = md5.hexdigest()
    try:
        user = models.Users(email=user_data.email, password_hash=password_hash, balance=0)
        db.add(user)
        db.flush()
        token = jwt.encode({"user_id": user.id}, salt, algorithm="HS256")
        db.commit()

    except IntegrityError:
        raise HTTPException(400, "this email is already taken")
    return token


def sign_user(db: Session, user_data: schemas.UserCreate):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode('utf-8'))
    password_hash = md5.hexdigest()
    hash_in_db = db.query(models.Users.password_hash).filter(models.Users.login == user_data.email).first()
    if hash_in_db is None:
        raise HTTPException(401, "invalid login")
    if password_hash == hash_in_db[0]:
        user_id = db.query(models.Users.id).filter(models.Users.login == user_data.email).first()[0]
        token = jwt.encode({"user_id": user_id}, salt, algorithm="HS256")
        return token
    raise HTTPException(401, "invalid password")


def get_user(db: Session, user_id):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def gen_code(db: Session, email):

    if db.query(models.Users.is_confirm).filter(models.Users.email == email).first()[0]:
        return schemas.BaseResponse(status="False", msg="email is confirm")

