from fastapi import APIRouter, Depends, status, HTTPException

from ...models.user import User, ChangeDefaultModel, ChangeUserPlan, UserOutput
from ...models.responses import ResponseStatus
from ...dependencies.dependencies import *

from ....database.db import DBHelper


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=UserOutput, status_code=200, responses={401: {"model": ResponseStatus}})
async def get_user(
    user_id: int,
    db: DBHelper = Depends(get_db),
    ):

    user = db.get_user(user_id)
    if not user:
        return {"status": status.HTTP_401_UNAUTHORIZED}
    return UserOutput(**user)

@router.put("/default_model", responses={200: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def change_model(
    # change_model: ChangeDefaultModel,
    user_id: int,
    model_id: int,
    db: DBHelper = Depends(get_db),
    ):
    db.update_default_model(
        user_id,
        model_id,
    )
    return {"status": status.HTTP_200_OK}

@router.put("/plan", responses={200: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def change_plan(
    # plan: ChangeUserPlan,
    user_id: int,
    plan: str,
    db: DBHelper = Depends(get_db),
    ):
    db.update_plan(
        user_id,
        plan,
    )
    return {"status": status.HTTP_200_OK}
