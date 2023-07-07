from pydantic import BaseModel


class Conversation(BaseModel):
    user_id: int
    convo_id: int

class NewConversation(BaseModel):
    user_id: int
    name: str
    model_id: int

class Msg(BaseModel):
    user_id: int
    convo_id: int
    question: str
    answer: str

class Bot(BaseModel):
    user_id: int
    name: str
    system_name: str
    model_id: int
    model: str
    prompt: str