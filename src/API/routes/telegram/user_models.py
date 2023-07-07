from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.exceptions import HTTPException

from ...models.model import UserModel
from ...dependencies.dependencies import *

from ....database.db import DBHelper


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/count")
async def get_count_models(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_model_count(
        user_id,
    )
    return {
        "user_id": user_id,
        "models": count,
    }


@router.get("/")
async def get_user_models(
    user_id: int,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
    ) -> UserModel:
    user = db.get_user(user_id)
    if not user:
        return {"status": status.HTTP_401_UNAUTHORIZED}
    user_models = db.get_user_models(user_id, offset, limit)
    return user_models

@router.post("/new")
async def add_user_model(
    model: UserModel,
    db: DBHelper = Depends(get_db),
    ):
    if not db.get_user(model.user_id):
        return {"status": status.HTTP_401_UNAUTHORIZED}
    user_id = user.get("user_id")
    db.add_user_model(
        model.user_id,
        model.name,
        model.system_name,
        model.base_model_id,
        model.prompt,
    )
    return {"status": status.HTTP_201_CREATED}