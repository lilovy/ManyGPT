from fastapi import APIRouter, WebSocket, Depends, Request
from typing import List

from ...models.message import Message, MessageFull
from ...models.model import ModelBase
from ...models.responses import ResponseStatus

from ....core.llms import LLMs
from ....database.db import DBHelper
from ...dependencies.dependencies import *


router = APIRouter(prefix="/core", tags=["core"])


@router.websocket("/ws")
async def ask_ws(
    ws: WebSocket,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
    ):
    await ws.accept()

    while True:
        content = await ws.receive_json()
        message = Message(**content)

        access = db.can_user_ask_question(
            message.user_id,
        )

        if access:
            msg = llm.ask(
                message.request,  
                message.model,
                flush=True,
                )

            full_response = ""
            for chunk in msg:
                full_response += chunk
                await websocket.send_text(chunk)

            db.add_message(
                message.convo_id,
                message.request,
                full_response,
            )

            await websocket.send_text("<br><br>")
        


@router.post("/ask")
async def ask(
    # request: Request,
    # message: Message,
    user_id: int,
    model: str,
    convo_id: int,
    request: str,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
):

    access = db.can_user_ask_question(
        user_id,
    )

    if access:
        content = llm.ask(
            request,
            model,
        )

        for response in content:
            pass

        db.add_message(
            convo_id,
            request,
            response,
        )

        return MessageFull(**message, response=response)
    return {"status": "No token"}


@router.get("/base_models")
async def ask(
    db: DBHelper = Depends(get_db),
):
    base_models = db.get_base_model()

    return base_models