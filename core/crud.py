from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from core import models, schemas, smtp

import random
import string
import jwt

import hashlib
from configs import salt


def get_cases(db: Session):
    return db.query(models.Cases).all()


def gen_code():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(5))


def check_code(code, user_id, db: Session):
    if code == db.query(models.Users.code).filter(models.Users.id == user_id).first()[0]:
        db.query(models.Users).filter(models.Users.id == user_id).update({"is_activate": True})
        db.commit()
        return
    raise HTTPException(400, "invalid code")


def change_code(user_id, db: Session):
    code = gen_code()
    db.query(models.Users).filter(models.Users.id == user_id).update({"code": code})
    db.commit()
    email = db.query(models.Users.email).filter(models.Users.id == user_id).first()[0]
    smtp.send_code(code, email)


def add_user(db: Session, user_data: schemas.UserCreate):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode('utf-8'))
    password_hash = md5.hexdigest()
    code = gen_code()
    try:
        user = models.Users(email=user_data.email, password_hash=password_hash, balance=0, is_activate=False, code=code)
        db.add(user)
        db.flush()
        token = jwt.encode({"user_id": user.id}, salt, algorithm="HS256")
        db.commit()

    except IntegrityError:
        raise HTTPException(400, "this email is already taken")
    smtp.send_code(code, user_data.email)
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


def get_user(db: Session, user_id) -> schemas.UserInfo:
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def check_email(db: Session, email):
    return db.query(models.Users.email).filter(models.Users.email == email).first() is not None
