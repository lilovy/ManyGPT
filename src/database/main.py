from .db import DBHelper
from config import db_path

db = DBHelper(db_path)
# db.create_db()

def get_db() -> DBHelper:
    # db = DBHelper(db_path)
    yield db
