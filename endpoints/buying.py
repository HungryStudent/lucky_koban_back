from fastapi import APIRouter, Depends, Request

from typing import List
from sqlalchemy.orm import Session
from yookassa import payment
from core.database import SessionLocal
from core import crud, payment
from core import schemas
from core.jwt_funcs import get_info_token

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/buy/{case_id}', response_model=schemas.PayUrl)
async def get_url_for_buy(case_id, db: Session = Depends(get_db), user_id: str = Depends(get_info_token)):
    case = crud.get_case(case_id, db)
    return schemas.PayUrl(url=payment.gen_pay(user_id, case))


@router.post('/buy/successful_pay', status_code=200)
async def give_case(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    buy_data: schemas.BuyData = schemas.BuyData(user_id=data["object"]["metadata"]["user_id"],
                                                case_id=data["object"]["metadata"]["case_id"])
    crud.add_case_to_user(buy_data, db)
