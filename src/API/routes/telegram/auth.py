from fastapi import Depends, APIRouter, status
from pydantic import ValidationError

from .user import User
from ...dependencies.dependencies import *
from ...middleware import middleware

from ....database.db import DBHelper


router = APIRouter(prefix="/auth", tags=["login"])

@router.post("/login", status_code=201)
async def login(
    # user: User,
    user_id: int,
    username: str,
    db: DBHelper = Depends(get_db),
    ):

    db.add_user(
        user_id,
        username,
        )

    return {}, 201
