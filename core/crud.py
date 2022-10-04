from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from core import models, schemas

import jwt
import hashlib

salt = "domoi"


def get_cases(db: Session):
    return db.query(models.Cases).all()


def add_user(db: Session, user_data: schemas.UserCreate):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode('utf-8'))
    password_hash = md5.hexdigest()
    try:
        db.add(models.Users(login=user_data.login, password_hash=password_hash))
        db.commit()
    except IntegrityError:
        return schemas.RegResponse(status=False, msg="this login is already taken")
    return schemas.RegResponse(status=True, msg="registration is successful")


def sign_user(user_data: schemas.UserCreate, db: Session):
    md5 = hashlib.md5()
    md5.update((user_data.password + salt).encode('utf-8'))
    password_hash = md5.hexdigest()
    hash_in_db = db.query(models.Users.password_hash).filter(models.Users.login == user_data.login).first()
    if hash_in_db is None:
        return schemas.SignResponse(status=False, msg="invalid login")
    if password_hash == hash_in_db[0]:
        user_id = db.query(models.Users.id).filter(models.Users.login == user_data.login).first()[0]
        token = jwt.encode({"user_id": user_id}, salt, algorithm="HS256")
        return schemas.SignResponse(status=True, msg="sign is successful", token=token)
    return schemas.SignResponse(status=False, msg="invalid password")