from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException

from ...models.user import ChangeUserPlan
from ...models.subscription import Subscription
from ...dependencies.dependencies import get_db
from ...middleware import middleware

from ....database.db import DBHelper


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/limits")
def change_limits(
    token: str,
    plan: Subscription,
    db: DBHelper = Depends(get_db),
    ):
    payload = middleware.decode_token(token)
    payload_secret = payload.get("status")

    if not payload_secret or payload_secret == status.HTTP_401_UNAUTHORIZED:
        return payload_secret
    db.update_limits(
        plan.name,
        plan.limit,
    )
    return {"status": status.HTTP_200_OK}


@router.post("/access")
def give_access(
    token: str,
    plan: ChangeUserPlan,
    db: DBHelper = Depends(get_db),
    ):
    payload = middleware.decode_token(token)
    payload_secret = payload.get("status")

    if not payload_secret or payload_secret == status.HTTP_401_UNAUTHORIZED:
        return payload_secret

    db.update_plan(
        plan.user_id,
        plan.plan_id,
    )
    return {"status": status.HTTP_200_OK}


@router.get("/stats")
def view_stats():
    ...