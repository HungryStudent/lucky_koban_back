from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class Code(BaseModel):
    code: str


class GamesToCase(BaseModel):
    case_id: int
    games_id: List[int]


class Email(BaseModel):
    email: str


class UserInfo(BaseModel):
    email: str
    balance: str

    class Config:
        orm_mode = True


class Case(BaseModel):
    id: int
    name: str
    price: int
    old_price: Union[int, None]

    class Config:
        orm_mode = True


class AuthResponse(BaseModel):
    status: str
    msg: str
    token: str = None


class BaseResponse(BaseModel):
    status: str
    msg: str
