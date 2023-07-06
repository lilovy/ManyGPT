from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.exceptions import HTTPException

from ...models.model import UserModel
from ...dependencies.dependencies import *

# from ....database.db import DBHelper


router = APIRouter(prefix="/models", tags=["models"])

@router.get("/")
def get_user_models(
    request: Request,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    # db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth

    user_id = user.get("user_id")
    user_models = db.get_user_models(user_id, offset, limit)
    return user_models

@router.post("/new")
def add_user_model(
    request: Request,
    model: UserModel,
    # db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != model.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    db.add_user_model(
        model.user_id,
        model.name,
        model.system_name,
        model.base_model_id,
        model.prompt,
    )
    return {"status": status.HTTP_201_CREATED}