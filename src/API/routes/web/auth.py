from fastapi import Depends, APIRouter, Form, Response, status

from .user import User
from ...dependencies.dependencies import *
from ...middleware import middleware

from ....database.db import DBHelper


router = APIRouter(prefix="/auth", tags=["login"])

@router.post("/login", status_code=201)
async def login(
    response: Response,
    # user: User,
    user_id: int = Form(...),
    username: str = Form(...),
    db: DBHelper = Depends(get_db),
    ):
    access_token_payload = {
        "status": status.HTTP_200_OK,
        "id": user_id,
        "username": username,
    }

    access_token = middleware.generate_token(access_token_payload)

    headers = {"Authorization": f"Bearer {access_token}"}
    response.set_cookie(key="access_token", value=access_token)

    db.add_user(user_id, username)

    return {}, 201, headers
