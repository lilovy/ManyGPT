from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.exceptions import HTTPException

from ....core.llms import LLMs
from ...models.model import UserModel, UserModelOutput
from ...models.responses import ResponseStatus
from ...models.count import Count
from ...dependencies.dependencies import *

from ....database.db import DBHelper


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/count", response_model=Count, status_code=200)
async def get_count_models(
    request: Request,
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    count = db.get_model_count(
        user_id,
    )
    return Count(
        user_id=user_id,
        object="models",
        count=count,
    ) 


@router.get("/", response_model=list[UserModelOutput], status_code=200, responses={401: {"model": ResponseStatus}})
async def get_user_models(
    request: Request,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth

    user_id = user.get("user_id")
    user_models = db.get_user_models(user_id, offset, limit)
    return [UserModelOutput(**models) for models in user_models]

@router.post("/new", responses={201: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def add_user_model(
    request: Request,
    model: UserModel,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != model.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

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