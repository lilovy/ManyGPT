from fastapi import APIRouter, Depends, Request, status, Response
from fastapi.exceptions import HTTPException

from ...models.user import ChangeUserPlan
from ...models.subscription import Subscription
from ...models.responses import ResponseStatus
from ...dependencies.dependencies import get_db
from ....core.graphs import bar_chart
from ...middleware import middleware

from ....database.db import DBHelper


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/limits")
async def change_limits(
    token: str,
    # plan: Subscription,
    name: str,
    limit: str,
    db: DBHelper = Depends(get_db),
    ):
    payload = middleware.decode_token(token)
    payload_secret = payload.get("status")

    if not payload_secret or payload_secret == status.HTTP_401_UNAUTHORIZED:
        return payload_secret
    db.update_limits(
        name,
        limit,
    )
    return {"status": status.HTTP_200_OK}


@router.post("/access")
async def give_access(
    token: str,
    # plan: ChangeUserPlan,
    user_id: int,
    plan: str,
    db: DBHelper = Depends(get_db),
    ):
    payload = middleware.decode_token(token)
    payload_secret = payload.get("status")

    if not payload_secret or payload_secret == status.HTTP_401_UNAUTHORIZED:
        return payload_secret

    db.update_plan(
        plan.user_id,
        plan.plan,
    )
    return {"status": status.HTTP_200_OK}


@router.get("/stats")
async def view_stats(
    db: DBHelper = Depends(get_db),
):
    # users_count = db.get_user_count_for_statistic()

    buff = bar_chart({"free": 3, "basic": 34, "advanced": 1})
    name = "293r"

    return Response(
        content=buff,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt",
            "filename": f"{name}.txt",
        }
    )