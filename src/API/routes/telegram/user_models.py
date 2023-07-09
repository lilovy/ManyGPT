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


@router.get("/count", status_code=200)
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
    return [UserModelOutput(**models) for models in user_models]

@router.post("/new")
async def add_user_model(
    # model: UserModel,
    user_id: int,
    base_model_id: int,
    name: str,
    system_name: str,
    prompt: str,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):
    if not db.get_user(user_id):
        return {"status": status.HTTP_401_UNAUTHORIZED}
    user_id = user.get("user_id")

    base_model = db.get_base_model(base_model_id)

    llm.new_bot(
        system_name,
        prompt,
        base_model,
    )

    db.add_user_model(
        user_id,
        name,
        system_name,
        base_model_id,
        prompt,
    )
    return {"status": status.HTTP_201_CREATED}