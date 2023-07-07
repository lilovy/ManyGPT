from pydantic import BaseModel


class Message(BaseModel):
    user_id: int
    convo_id: int
    request: str
    model: str

class MessageFull(Message):
    response: str