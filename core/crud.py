from sqlalchemy.orm import Session
from core import models, schemas


def get_cases(db: Session):
    return db.query(models.Cases).all()
