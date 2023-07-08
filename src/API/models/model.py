from pydantic import BaseModel
from enum import Enum

class UserModel(BaseModel):
    user_id: int
    name: str
    system_name: str
    base_model_id: int
    model: str
    prompt: str

class ModelBase(BaseModel):
    id: int
    name: str

class UserModelOutput(BaseModel):
    id: int
    user_id: int
    name: str
    system_name: str
    model: ModelBase
    prompt: str
    is_default: bool