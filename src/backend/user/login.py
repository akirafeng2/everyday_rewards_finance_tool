from .database_actions import UserDatabaseConnection
from ..database import db_conn
from werkzeug.datastructures import MultiDict




@db_conn(UserDatabaseConnection)
def get_user_info(DB_CONN: UserDatabaseConnection, login_dict: MultiDict) -> tuple:
    nickname = login_dict['name']
    household_name = login_dict['household']
    with DB_CONN:
        user_info = DB_CONN.get_user_info(nickname, household_name)
    return user_info
    
