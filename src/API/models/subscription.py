from pydantic import BaseModel
from enum import Enum


class Subscription(BaseModel):
    name: str
    limit: int


class Subs(Enum):
    free = "free"
    basic = "basic"
    advanced = "advanced"