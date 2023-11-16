from .database_actions import UserDatabaseConnection
from ..common import db_conn


@db_conn(UserDatabaseConnection)
def get_user_info(DB_CONN: UserDatabaseConnection, login_name: str):
    """Takes in the MultiDict result from the login route and returns the a\
    tuple of the user's profile_id, household_id, user_name, and\
    household_name"""
    with DB_CONN:
        user_info = DB_CONN.get_user_info(login_name)
    return user_info


@db_conn(UserDatabaseConnection)
def get_household_profiles(DB_CONN: UserDatabaseConnection):
    with DB_CONN:
        result = DB_CONN.get_household_names()
    return result
