from fastapi import APIRouter, Depends, Request, status, Query
from typing import List

from ....core.llms import LLMs
from ...models.conversation import Conversation, NewConversation, Msg, Bot, ConversationOutput, Messages
from ...models.responses import ResponseStatus
from ...models.count import Count
from ...models.message import Message

from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.get("/count", response_model=Count, status_code=200)
async def get_count_msg(
    request: Request,
    msg: Conversation,
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")
    count = db.get_message_count(
        msg.user_id,
        msg.convo_id,
    )
    return Count(
        user_id=user_id,
        object="messages",
        count=count,
    )


@router.get("/", response_model=List[Messages], status_code=200)
async def get_conversation(
    request: Request,
    conversation: Conversation,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
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

    return [Messages(**msg) for msg in content]


@router.get("/all", response_model=List[ConversationOutput], status_code=200)
async def get_conversations(
    request: Request,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")

    content = db.get_user_conversations(
        user_id,
        offset,
        limit
    )

    return [ConversationOutput(**convo) for convo in content]


@router.get("/all/count", response_model=Count, status_code=200)
async def get_count_conversations(
    request: Request,
    db: DBHelper = Depends(get_db),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth

    user_id = request.state.user.get("user_id")

    count = db.get_count_conversation(
        user_id,
    )

    return Count(
        user_id=user_id,
        object="conversations",
        count=count,
    )


@router.post("/new", responses={201: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def add_conversation(
    request: Request,
    conversation: NewConversation,
    db: DBHelper = Depends(get_db),
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


@router.post("/new/bot", responses={201: {"model": ResponseStatus}, 401: {"model": ResponseStatus}})
async def add_bot(
    request: Request,
    bot: Bot,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
):
    if request.state.auth.get("status") != status.HTTP_200_OK:
        return request.state.auth
    user = request.state.auth
    user_id = user.get("user_id")
    if user_id != conversation.user_id:
        return {"status": status.HTTP_401_UNAUTHORIZED}

    llm.new_bot(
        bot.name,
        bot.prompt,
        bot.model,
    )

    db.add_user_model(
        bot.user_id,
        bot.name,
        bot.system_name,
        bot.model_id,
        bot.prompt,
    )

    return {"status": status.HTTP_201_CREATED}


# @router.post("/msg")
# async def add_msg(
#     request: Request,
#     msg: Msg,
#     db: DBHelper = Depends(get_db),
# ):
#     if request.state.auth.get("status") != status.HTTP_200_OK:
#         return request.state.auth
#     user = request.state.auth
#     user_id = user.get("user_id")
#     if user_id != msg.user_id:
#         return {"status": status.HTTP_401_UNAUTHORIZED}

#     access = db.can_user_ask_question(
#         msg.user_id,
#     )

#     if access:
#         db.add_message(
#             msg.convo_id,
#             msg.question,
#             msg.answer,
#         )
#         return {"status": status.HTTP_201_CREATED}
#     return {"status": "no tokens"}

