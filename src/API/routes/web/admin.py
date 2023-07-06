from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException

from ...dependencies.dependencies import *
from ...models.model import UserModel

# from ....database.db import DBHelper


router = APIRouter(prefix="/admin", tags=["admin"])

