from .db import DBHelper
from config import db_path

def get_db() -> DBHelper:
    db = DBHelper(db_path)
    yield db