# from src.API.dependencies.dependencies import get_db
from src.database.db import DBHelper


db = DBHelper("src\database\multigpt.db")
# for db in get_db():
#     ...
db.add_user(123, "sdfsdf")