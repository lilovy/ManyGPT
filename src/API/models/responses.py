from pydantic import BaseModel
from typing import Union


class ResponseStatus(BaseModel):
    status: Union[int, str]