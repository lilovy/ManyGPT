from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

class ChangeDefaultModel(BaseModel):
    user_id: int
    model_id: int

class ChangeUserPlan(BaseModel):
    user_id: int
    plan_id: int

