from .db import DBHelper

def get_db():
    db = DBHelper()
    yield db