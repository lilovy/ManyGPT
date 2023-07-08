from fastapi import APIRouter, Depends, Request, status, Query

from ...models.conversation import Conversation, NewConversation, Msg, Bot, ConversationOutput, Messages
from ...models.responses import ResponseStatus
from ...models.count import Count
from ....core.llms import LLMs
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.get("/count", response_model=Count, status_code=200)
async def get_count_msg(
    msg: Conversation,
    db: DBHelper = Depends(get_db),
):
    count = db.get_message_count(
        msg.user_id,
        msg.convo_id,
    )

    return Count(
        user_id=user_id,
        object="messages",
        count=count,
    )


@router.get("/", response_model=list[Messages], status_code=200)
async def get_conversation(
    conversation: Conversation,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
):

    content = db.get_user_msg_history(
        conversation.convo_id,
        offset,
        limit
    )

    return [Messages(**msg) for msg in content]


@router.get("/all", response_model=list[ConversationOutput], status_code=200)
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


@router.get("/all/count", response_model=Count, status_code=200)
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


@router.post("/new", responses={201: {"model": ResponseStatus}})
async def add_conversation(
    conversation: NewConversation,
    db: DBHelper = Depends(get_db),
):
    db.add_chat(
        conversation.user_id,
        conversation.name,
        conversation.model_id,
    )

    return ResponseStatus(status=status.HTTP_201_CREATED)


@router.post("/new/bot", responses={201: {"model": ResponseStatus}})
async def add_bot(
    bot: Bot,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
):
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


