from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str

class UserInfo(BaseModel):
    login: str
    balance: str

class Case(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


class AuthResponse(BaseModel):
    status: str
    msg: str
    token: str = None
