from fastapi import APIRouter, Body, Depends, status, HTTPException, Request
from pydantic import BaseModel

from ...models.user import User, ChangeDefaultModel, ChangeUserPlan, UserOutput
from ...models.responses import ResponseStatus
from ...dependencies.dependencies import * 
from ...middleware import middleware

from ....database.db import DBHelper
from sqlalchemy.orm import Session


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=UserOutput, status_code=200, responses={401: {"model": ResponseStatus}})
async def get_user(
    request: Request,
    db: DBHelper = Depends(get_db),
    ):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.auth.get("user_id")
    user = db.get_user(user_id)

    return UserOutput(**user)

@router.put("/default_model", responses={200: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def change_model(
    request: Request,
    model: ChangeDefaultModel,
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != model.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}
    db.update_default_model(
        model.user_id,
        model.model_id,
    )
    return {"status": status.HTTP_200_OK}


@router.put("/plan", responses={200: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def change_plan(
    request: Request,
    plan: ChangeUserPlan,
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != plan.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}
    db.update_plan(
        plan.user_id,
        plan.plan,
    )
    return {"status": status.HTTP_200_OK}
