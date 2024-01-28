from .database_actions import UserDatabaseConnection
from ..common import db_conn
from .md5_hash import hash_string_md5


@db_conn(UserDatabaseConnection)
def get_user_info(DB_CONN: UserDatabaseConnection, login_email: str, password: str) -> dict:
    """Takes in a user's email and password. If credentials are correct, returns a\
    tuple of the user's profile_id, household_id, user_name, and\
    household_name. If credentials is not correct, returns error"""
    hash_password = hash_string_md5(password)
    with DB_CONN:
        user_info = DB_CONN.get_user_info(login_email, hash_password)
    data_titles = ('profile_id', 'household_id', 'user_name', 'household_name')
    login_info_dict = dict(zip(data_titles, user_info))
    return login_info_dict


@db_conn(UserDatabaseConnection)
def get_household_profiles(DB_CONN: UserDatabaseConnection):
    with DB_CONN:
        result = DB_CONN.get_household_names()
    return result
