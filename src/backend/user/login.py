from .database_actions import UserDatabaseConnection
from ..database import db_conn
from werkzeug.datastructures import MultiDict


@db_conn(UserDatabaseConnection)
def get_user_info(DB_CONN: UserDatabaseConnection, login_dict: MultiDict):
    """Takes in the MultiDict result from the login route and returns the a\
    tuple of the user's profile_id, household_id, user_name, and\
    household_name"""
    user_name = login_dict['name']
    household_name = login_dict['household']
    with DB_CONN:
        user_info = DB_CONN.get_user_info(user_name, household_name)
    return user_info
