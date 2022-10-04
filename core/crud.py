from sqlalchemy.orm import Session
from core import models, schemas

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
    except:
        return
