from .database_actions import UserDatabaseConnection
from ..common import db_conn


@db_conn(UserDatabaseConnection)
def user_exists(DB_CONN, username: str) -> bool:
    with DB_CONN:
        user_details = DB_CONN.get_user_info(username)
    if user_details:
        return True
    else:
        return False


@db_conn(UserDatabaseConnection)
def add_profile(DB_CONN, profile_id: str, username: str) -> None:
    with DB_CONN:
        DB_CONN.add_profile_into_db(profile_id, username)
        DB_CONN.commit_changes()
