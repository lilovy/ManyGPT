import datetime
from typing import Any

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy import Column, Integer, Identity, ForeignKey, DateTime, String, Text, Boolean, Enum, BLOB, LargeBinary
from src.database.model.enums import *


engine = sqlalchemy.create_engine('sqlite:///multigpt.db', echo=True)


class Base(DeclarativeBase):
    @classmethod
    def create_db(cls, some_engine):
        cls.metadata.create_all(bind=some_engine)


class Conversation(Base):
    __tablename__ = "Conversations"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    name = Column(String)
    llm_id = Column(Integer, ForeignKey("UserLLMs.id"))

    user = relationship("User", back_populates="conversation")
    user_llm = relationship("UserLLM", back_populates="conversation")
    message = relationship("Message", back_populates="conversation")
    curr_convo = relationship("CurrConvo", back_populates="conversation")

    def __init__(self,  user_id: int, name: str, llm_id: int, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.name = name
        self.llm_id = llm_id

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }


class FilePart(Base):
    __tablename__ = "FileParts"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(Integer, ForeignKey("Projects.id"))
    part = Column(Text)
    is_used = Column(Boolean)

    project = relationship("Project", back_populates="file_part")

    def __init__(self, part: str, project_id: int, **kw: Any):
        super().__init__(**kw)
        self.part = part
        self.is_used = False
        self.project_id = project_id

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "part": self.part,
            "is_used": self.is_used
        }


class LLM(Base):
    __tablename__ = "LLMs"

    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model = Column(Enum(ModelEnum))

    user_llm = relationship("UserLLM", back_populates="llm")
    project_llm = relationship("ProjectLLM", back_populates="llm")

    def __init__(self, model: ModelEnum, **kw: Any):
        super().__init__(**kw)
        self.model = model

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "model": self.model
        }


class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    time = Column(DateTime)
    conversation_id = Column(Integer, ForeignKey("Conversations.id"))

    conversation = relationship("Conversation", back_populates="message")

    def __init__(self, question: str, answer: str, conversation_id: int, **kw: Any):
        super().__init__(**kw)
        self.question = question
        self.answer = answer
        self.time = datetime.datetime.now()
        self.conversation_id = conversation_id

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "content": {
                "question": self.question,
                "answer": self.answer
            },
            "time": self.time
        }


class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    model_id = Column(Integer, ForeignKey("ProjectLLMs.id"))
    name = Column(String)
    mimetype = Column(String)
    file = Column(LargeBinary)

    user = relationship("User", back_populates="project")
    file_part = relationship("FilePart", back_populates="project")
    result_data = relationship("ResultData", back_populates="project")
    project_llm = relationship("ProjectLLM", back_populates="project")

    def __init__(self, user_id: int, model_id: int, name: str, mimetype: str, file: bytes, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.name = name
        self.mimetype = mimetype
        self.file = file
        self.model_id = model_id

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "mimetype": self.mimetype
        }


class ProjectLLM(Base):
    __tablename__ = "ProjectLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    model_id = Column(Integer, ForeignKey("LLMs.id"))
    system_name = Column(String)
    prompt = Column(Text)

    project = relationship("Project", back_populates="project_llm")
    llm = relationship("LLM", back_populates="project_llm")

    def __init__(self, model_id: int, system_name: str, prompt: str, **kw: Any):
        super().__init__(**kw)
        self.model_id = model_id
        self.system_name = system_name
        self.prompt = prompt

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "system_name": self.system_name,
            "prompt": self.prompt
        }


class ResultData(Base):
    __tablename__ = "ResultData"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    project_id = Column(ForeignKey("Projects.id"))
    data = Column(Text)

    project = relationship("Project", back_populates="result_data")

    def __init__(self, project_id: int, data: str, **kw: Any):
        super().__init__(**kw)
        self.project_id = project_id
        self.data = data

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "data": self.data
        }


class SubscriptionType(Base):
    __tablename__ = "SubscriptionTypes"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    name = Column(Enum(SubscriptionLevelEnum))
    limit = Column(Integer)

    user = relationship("User", back_populates="subscription_type")

    def __init__(self, name: SubscriptionLevelEnum, limit: int, **kw: Any):
        super().__init__(**kw)
        self.name = name
        self.limit = limit

    def get_simple_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "limit": self.limit
        }


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    registration_date = Column(DateTime)
    subscription_id = Column(Integer, ForeignKey("SubscriptionTypes.id"))

    user_token = relationship("UserToken", back_populates="user")
    project = relationship("Project", back_populates="user")
    user_llm = relationship("UserLLM", back_populates="user")
    conversation = relationship("Conversation", back_populates="user")
    subscription_type = relationship("SubscriptionType", back_populates="user")

    curr_convo = relationship("CurrConvo", back_populates="user")

    def __init__(self, user_id: int, username, subscription_type_id: int, **kw: Any):
        super().__init__(**kw)
        self.id = user_id
        self.username = username
        self.registration_date = datetime.datetime.now()
        self.subscription_id = subscription_type_id

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "registration_date": self.registration_date
        }


class UserLLM(Base):
    __tablename__ = "UserLLMs"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    base_model_id = Column(Integer, ForeignKey("LLMs.id"))
    name = Column(String)
    system_name = Column(String)
    prompt = Column(Text)
    is_default = Column(Boolean)

    llm = relationship("LLM", back_populates="user_llm")
    user = relationship("User", back_populates="user_llm")
    conversation = relationship("Conversation", back_populates="user_llm")

    def __init__(self, user_id: int, name: str, system_name: str,
                 base_model_id: int, prompt: str, is_default: bool, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.base_model_id = base_model_id
        self.name = name
        self.system_name = system_name
        self.prompt = prompt
        self.is_default = is_default

    def get_simple_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

    def get_full_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "user_id":self.user_id,
            "system_name": self.system_name,
            "prompt": self.prompt,
            "is_default": self.is_default
        }


class UserToken(Base):
    __tablename__ = "UserToken"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    count = Column(Integer)
    last_update = Column(DateTime)

    user = relationship("User", back_populates="user_token")

    def __init__(self, user_id: int, count: int, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.count = count
        self.last_update = datetime.date.today()

    def get_simple_dict(self) -> dict:
        return {
            "count": self.count,
            "last_update": self.last_update
        }


class CurrConvo(Base):
    __tablename__ = "CurrConvo"
    id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    convo_id = Column(Integer, ForeignKey("Conversations.id"))

    user = relationship("User", back_populates="curr_convo")
    conversation = relationship("Conversation", back_populates="curr_convo")

    def __init__(self,  user_id: int, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.convo_id = None
