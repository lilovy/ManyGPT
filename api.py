from typing import Union, List
from fastapi import FastAPI, Depends, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from datetime import datetime
import uvicorn

from src.core.llms import LLMs
import json
import random


app = FastAPI()
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
templates = Jinja2Templates(directory="src/frontend/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()

    client = LLMs("o6BvUBrXYXuis5Xb5Y1CLg%3D%3D")

    while True:
        message = await websocket.receive_text() 
        msg = client.ask(message, flush=True)
        full_response = ""
        for chunk in msg:
            full_response += chunk
            await websocket.send_text(chunk)
        
        await websocket.send_text("<br><br>")


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)