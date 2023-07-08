from pydantic import BaseModel


class Count(BaseModel):
    user_id: int
    object: str
    count: int