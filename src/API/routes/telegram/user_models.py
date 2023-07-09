from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.exceptions import HTTPException
from typing import List

from ....core.llms import LLMs
from ...models.model import UserModel, UserModelOutput
from ...models.responses import ResponseStatus
from ...models.count import Count
from ...dependencies.dependencies import *

from ....database.db import DBHelper


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/count", response_model=Count, status_code=200)
async def get_count_models(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_model_count(
        user_id,
    )
    return Count(
        user_id=user_id,
        object="models",
        count=count,
    )


@router.get("/", response_model=List[UserModelOutput], status_code=200, responses={401: {"model": ResponseStatus}})
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
    return [UserModelOutput(**models) for models in user_models]

@router.post("/new", responses={201: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def add_user_model(
    model: UserModel,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):
    if not db.get_user(model.user_id):
        return {"status": status.HTTP_401_UNAUTHORIZED}
    user_id = user.get("user_id")

    llm.new_bot(
        model.system_name,
        model.prompt,
        model.model,
    )

    db.add_user_model(
        model.user_id,
        model.name,
        model.system_name,
        model.base_model_id,
        model.prompt,
    )
    return {"status": status.HTTP_201_CREATED}