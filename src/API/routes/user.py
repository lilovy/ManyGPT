from fastapi import APIRouter, Body
from src.API.schemes.user import User
from dependencies import get_db
from .db.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users():
    return [
        {
            "id": 2,
            "name": "John"
        },
    ]

@router.get("/user/{user_id}")
def get_user(user_id):
    return {
        "id": user_id,
        "user": "Ivan",
    }

@router.post("/create")
def create_user(user: User = Body(...)):
    ...