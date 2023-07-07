from pydantic import BaseModel
from fastapi import UploadFile


class UserProject(BaseModel):
    user_id: int
    project_id: int

class NewUserProject(BaseModel):
    user_id: int
    name: str
    mimetype: str
    model_id: int
    prompt: str
    file: UploadFile