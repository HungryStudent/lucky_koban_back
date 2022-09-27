from fastapi import APIRouter, Depends

from typing import List

from sqlalchemy.orm import Session

from core.database import SessionLocal
from core import crud
from core import schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/cases/get', response_model=List[schemas.Case])
async def get_cases(db: Session = Depends(get_db)):
    return crud.get_cases(db)