from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str


class Case(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


class RegResponse(BaseModel):
    status: str
    msg: str


class SignResponse(BaseModel):
    status: str
    msg: str
    token: str = None