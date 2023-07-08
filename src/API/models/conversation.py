from pydantic import BaseModel
from datetime import datetime


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

class MsgContent(BaseModel):
    question: str
    answer: str

class Convo(BaseModel):
    id: int
    name: str

class Messages(BaseModel):
    id: int
    content: MsgContent
    conversation: Convo
    time: datetime

class Bot(BaseModel):
    user_id: int
    name: str
    system_name: str
    model_id: int
    model: str
    prompt: str

class ConversationModel(BaseModel):
    id: int
    name: str
    system_name: str

class ConversationOutput(BaseModel):
    id: int
    user_id: int
    name: str
    llm: ConversationModel

class Conversations(BaseModel):
    conversation: list[ConversationOutput]