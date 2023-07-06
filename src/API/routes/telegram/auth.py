from fastapi import Depends, APIRouter, status

from .user import User
from ...dependencies.dependencies import *
from ...middleware import middleware

from ....database.db import DBHelper


router = APIRouter(prefix="/auth", tags=["login"])

@router.post("/login")
def login(
    user: User,
    # db: DBHelper = Depends(get_db),
    ):

    db.add_user(
        user.id,
        user.username,
        )

    return {"status": status.HTTP_201_CREATED}
