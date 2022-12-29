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


class Keys(BaseModel):
    game_id: int
    keys: List[str]


class Email(BaseModel):
    email: str


class UserInfo(BaseModel):
    email: str
    balance: str

    class Config:
        orm_mode = True


class Game(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Case(BaseModel):
    id: int
    name: str
    price: int
    old_price: Union[int, None]
    games: List[Game]

    class Config:
        orm_mode = True


class AuthResponse(BaseModel):
    status: str
    msg: str
    token: str = None


class BaseResponse(BaseModel):
    status: str
    msg: str
