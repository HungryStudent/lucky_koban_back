from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    password: str


class Case(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True