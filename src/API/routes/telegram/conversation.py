from fastapi import APIRouter, Depends, Request, status, Query

from ...models.conversation import Conversation, NewConversation, Msg, Bot
from ....core.llms import LLMs
from ...dependencies.dependencies import *
from ....database.db import DBHelper


router = APIRouter(prefix="/conversation", tags=["conversation"])


@router.get("/count")
async def get_count_msg(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_message_count(
        user_id,
    )

    return {
        "user_id": user_id,
        "messages": count,
    }


@router.get("/")
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

    return content


@router.get("/all")
async def get_conversations(
    user_id: int,
    conversation: Conversation,
    offset: int = Query (0, ge=0),
    limit: int = Query(10, ge=1),
    db: DBHelper = Depends(get_db),
):
    content = db.get_user_conversations(
        user_id,
        offset,
        limit
    )

    return content


@router.get("/all/count")
async def get_count_conversations(
    user_id: int,
    db: DBHelper = Depends(get_db),
):
    count = db.get_count_conversation(
        user_id,
    )

    return {
        "user_id": user_id,
        "conversations": count,
    }


@router.post("new")
async def add_conversation(
    conversation: NewConversation,
    db: DBHelper = Depends(get_db),
):
    db.add_chat(
        conversation.user_id,
        conversation.name,
        conversation.model_id,
    )

    return {"status": status.HTTP_201_CREATED}


@router.post("/new/bot")
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

    return {"status": status.HTTP_201_CREATED}


@router.post("msg")
async def add_msg(
    msg: Msg,
    db: DBHelper = Depends(get_db),
):

    db.add_message(
        msg.convo_id,
        msg.question,
        msg.answer,
    )

    return {"status": status.HTTP_201_CREATED}
