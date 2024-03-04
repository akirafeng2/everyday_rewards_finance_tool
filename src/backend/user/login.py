from .database_actions import UserDatabaseConnection
from ..common import db_conn


@db_conn(UserDatabaseConnection)
def get_user_info(DB_CONN: UserDatabaseConnection, user_id: str) -> dict:
    """Takes in a SU user_id returns a tuple of the user's profile_id, household_id, user_name, and household_name."""
    with DB_CONN:
        user_info = DB_CONN.get_user_info(user_id)

    data_titles = ('user_name', 'household_name')
    login_info_dict = dict(zip(data_titles, user_info))
    return login_info_dict


@db_conn(UserDatabaseConnection)
def get_household_profiles(DB_CONN: UserDatabaseConnection, user_id: str):
    with DB_CONN:
        result = DB_CONN.get_household_names(user_id)
    household_names = [name[0].capitalize() for name in result]
    return household_names
