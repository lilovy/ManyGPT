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


@router.get("/plans")
async def get_plans(
    db: DBHelper = Depends(get_db),
):
    plans = db.get_subs()
    return plans


@router.post("/limits")
async def change_limits(
    token: str,
    # plan: Subscription,
    # name: str,
    limit: str,
    db: DBHelper = Depends(get_db),
    ):
    payload = middleware.decode_token(token)
    payload_secret = payload.get("status")

    if not payload_secret or payload_secret == status.HTTP_401_UNAUTHORIZED:
        return payload_secret
    db.update_limits(
        # name,
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
    

    content = bar_chart(user_count, dict(x="Plan", y="Users"))
    name = datetime.now()

    return Response(
        content=content,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt",
            "filename": f"{name}.txt",
        }
    )


@router.get("/stats/growth")
async def get_user_growth(
    period: int = 7,
    plan: str = None,
    db: DBHelper = Depends(get_db),
):
    user_growth = db.user_growth(period=period, plan=plan)
    
    content = bar_chart(user_growth, dict(x="Date", y="New users"))
    
    name = datetime.now()

    return Response(
        content=content,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt",
            "filename": f"{name}.txt",
        }
    )


@router.get("/stats/interaction")
async def get_user_interaction(
    period: int = 7,
    db: DBHelper = Depends(get_db),
):
    amount_of_interaction = db.amount_of_interaction(period=period)

    content = bar_chart(amount_of_interaction, dict(x="Date", y="New messages"))

    name = datetime.now()

    return Response(
        content=content,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename={name}.txt",
            "filename": f"{name}.txt",
        }
    )