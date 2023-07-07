from fastapi import APIRouter, Depends, Request, status, Query

from ...models.conversation import Conversation, NewConversation, Msg

from ...dependencies.dependencies import *
# from ....database.db import DBHelper


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.get("/count")
def get_count_msg(
    request: Request,
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    count = db.get_message_count(
        user_id,
    )
    return {
        "user_id": user_id,
        "messages": count,
    }


@router.get("/")
def get_conversation(
    request: Request,
    conversation: Conversation,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    if user_id != conversation.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    content = db.get_user_msg_history(
        conversation.convo_id,
        offset,
        limit
    )

    return content


@router.get("/all")
def get_conversations(
    request: Request,
    conversation: Conversation,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")

    content = db.get_user_conversations(
        user_id,
        offset,
        limit
    )

    return content


@router.get("/all/count")
def get_count_conversations(
    request: Request,
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")

    count = db.get_count_conversation(
        user_id,
    )

    return {
        "user_id": user_id,
        "conversations": count,
    }


@router.post("/new")
def add_conversation(
    request: Request,
    conversation: NewConversation,
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != conversation.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    db.add_chat(
        conversation.user_id,
        conversation.name,
        conversation.model_id,
    )

    return {"status": status.HTTP_201_CREATED}


@router.post("/msg")
def add_msg(
    request: Request,
    msg: Msg,
    # db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != msg.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    db.add_message(
        msg.convo_id,
        msg.question,
        msg.answer,
    )

    return {"status": status.HTTP_201_CREATED}
