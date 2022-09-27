from typing import List, Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    password: str


class Case(BaseModel):
    name: str
    price: int
    old_price: int
    image_path: str