from fastapi import APIRouter, WebSocket, Depends, Request

from ...models.message import Message, MessageFull
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
        


@router.post("/ask", response_model=MessageFull, status_code=200, responses={404: {"model": ResponseStatus}})
async def ask(
    # request: Request,
    message: Message,
    db: DBHelper = Depends(get_db),
    llm: LLMs = Depends(get_llm),
):

    access = db.can_user_ask_question(
        message.user_id,
    )

    if access:
        content = llm.ask(
            message.request,
            message.model,
        )

        for response in content:
            pass

        db.add_message(
            message.convo_id,
            message.request,
            response,
        )

        return MessageFull(**message, response=response)
    return {"status": "No token"}
