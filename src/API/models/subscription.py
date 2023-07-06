from pydantic import BaseModel


class Subscription(BaseModel):
    name: str
    limit: int