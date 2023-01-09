import jwt
from fastapi import Cookie, HTTPException
from jwt import DecodeError

from configs import salt


def get_info_token(token: str = Cookie()):
    try:
        user_data = jwt.decode(token, salt, algorithms=["HS256"])
    except DecodeError:
        raise HTTPException(401, "invalid token")
    return user_data["user_id"]
