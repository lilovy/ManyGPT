from pydantic import BaseModel


class ResponseStatus(BaseModel):
    status: int | str