from fastapi import APIRouter, Depends, status, HTTPException

from ...models.user import User, ChangeDefaultModel, ChangeUserPlan
from ...dependencies.dependencies import *

# from ....database.db import DBHelper


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
def get_user(
    user: User,
    db: DBHelper = Depends(get_db),
    ):

    user = db.get_user(user.user_id)
    if not user:
        return {"status": status.HTTP_401_UNAUTHORIZED}
    return user

@router.put("/default_model")
def change_model(
    change_model: ChangeDefaultModel,
    db: DBHelper = Depends(get_db),
    ):
    db.update_default_model(
        change_model.user_id,
        change_model.model_id,
    )
    return {"status": status.HTTP_200_OK}

@router.post("/plan")
def change_plan(
    plan: ChangeUserPlan,
    db: DBHelper = Depends(get_db),
    ):
    db.update_plan(
        plan.user_id,
        plan.plan_id,
    )
    return {"status": status.HTTP_200_OK}
