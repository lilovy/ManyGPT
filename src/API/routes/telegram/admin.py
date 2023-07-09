from fastapi import APIRouter, Depends, Request, status, Response
from fastapi.exceptions import HTTPException
from datetime import datetime

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


@router.get("/stats/all_users")
async def get_all_users(
    db: DBHelper = Depends(get_db),
):
    user_count = db.get_user_count_for_statistic()

    content = bar_chart(users_count)
    name = datetime.now()

    return Response(
        content=content,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt",
            "filename": f"{d}.txt",
        }
    )


@router.get("/stats/growth")
async def