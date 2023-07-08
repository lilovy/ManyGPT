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
    model: str
    prompt: str
    file: UploadFile

class ProjectModel(BaseModel):
    id: int
    system_name: str
    prompt: str

class Projects(BaseModel):
    id: int
    user_id: int
    name: str
    model: ProjectModel
    mimetype: str