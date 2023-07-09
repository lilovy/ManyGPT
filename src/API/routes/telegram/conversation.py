from fastapi import APIRouter, Depends, Request, status, Query
from typing import List

from ...models.conversation import Conversation, NewConversation, Msg, Bot, ConversationOutput, Messages
from ...models.responses import ResponseStatus
from ...models.count import Count
from ....core.llms import LLMs
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.get("/count")
async def get_count_msg(
    # msg: Conversation,
    user_id: int,
    convo_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_message_count(
        # msg.user_id,
        convo_id,
    )

    return Count(
        user_id=user_id,
        object="messages",
        count=count,
    )


@router.get("/")
async def get_conversation(
    # conversation: Conversation,
    convo_id: int,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
):

    content = db.get_user_msg_history(
        convo_id,
        offset,
        limit
    )

    return [Messages(**msg) for msg in content]


@router.get("/all")
async def get_conversations(
    user_id: int,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
):
    content = db.get_user_conversations(
        user_id,
        offset,
        limit
    )

    return [ConversationOutput(**convo) for convo in content]


@router.get("/all/count")
async def get_count_conversations(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_count_conversation(
        user_id,
    )

    return Count(
        user_id=user_id,
        object="conversations",
        count=count,
    )


@router.post("/new")
async def add_conversation(
    # conversation: NewConversation,
    user_id: int,
    model_id: int,
    name: str,
    db: DBHelper = Depends(get_db),
):
    db.add_chat(
        user_id,
        name,
        model_id,
    )

    return ResponseStatus(status=status.HTTP_201_CREATED)


@router.post("/new/bot")
async def add_bot(
    # bot: Bot,
    user_id: int,
    name: str,
    system_name: str,
    model_id: int,
    # model: str,
    prompt: str,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
):
    model = db.get_base_model(model_id)

    llm.new_bot(
        system_name,
        prompt,
        model,
    )
    

    db.add_user_model(
        user_id,
        name,
        system_name,
        model_id,
        prompt,
    )

    return ResponseStatus(status=status.HTTP_201_CREATED)


# @router.post("msg")
# async def add_msg(
#     msg: Msg,
#     db: DBHelper = Depends(get_db),
# ):

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


