from fastapi import APIRouter, Depends, Cookie, HTTPException, File, UploadFile

from typing import List
from configs import true_admin_token
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


def check_admin_token(token):
    if token != true_admin_token:
        raise HTTPException(401, "invalid token")


@router.get('/cases/get', response_model=List[schemas.Case])
async def get_cases(db: Session = Depends(get_db)):
    return crud.get_cases(db)


@router.post('/cases/add', status_code=201)
async def add_case(admin_token: str = Cookie(), db: Session = Depends(get_db)):
    check_admin_token(admin_token)
    return {"message": "case is created"}


@router.post("/files")
async def create_upload_file(file: bytes = File()):
    with open("asd.png", "wb") as f:
        f.write(file)
    return {"filename": "ok"}


@router.get('/products/get', response_model=List[schemas.Case])
async def get_cases(db: Session = Depends(get_db)):
    return crud.get_cases(db)
