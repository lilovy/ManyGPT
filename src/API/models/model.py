from pydantic import BaseModel

class UserModel(BaseModel):
    user_id: int
    name: str
    system_name: str
    base_model_id: int
    prompt: str