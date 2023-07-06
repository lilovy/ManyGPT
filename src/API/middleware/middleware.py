from fastapi import Request, status
from fastapi.exceptions import HTTPException
import jwt

from config import access, JWT_ALGORITHM, JWT_SECRET


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return payload.copy()
    except:
        return {"status": status.HTTP_401_UNAUTHORIZED}


def generate_token(payload: dict):
    access_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return access_token


def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")

    if not token:
        request.state.auth = {"status": status.HTTP_401_UNAUTHORIZED}
    else:
        payload = decode_token(token)
        request.state.auth = payload

    return call_next(request)
