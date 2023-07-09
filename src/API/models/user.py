from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str

class ChangeDefaultModel(BaseModel):
    user_id: int
    model_id: int

class ChangeUserPlan(BaseModel):
    user_id: int
    plan: str

class Subscription(BaseModel):
    id: int
    name: str
    limit: str

class Token(BaseModel):
    count: int
    last_update: datetime

class DefaultModel(BaseModel):
    id: int
    name: str

class UserOutput(User):
    registration: datetime
    subscription: Subscription
    token: Token
    default_model: DefaultModel