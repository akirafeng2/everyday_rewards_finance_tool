from .database_actions import UserDatabaseConnection
from ..database import db_conn


@db_conn(UserDatabaseConnection)
def user_exists(DB_CONN, username: str) -> bool:
    with DB_CONN:
        user_details = DB_CONN.get_user_info(username)
    if user_details:
        return True
    else:
        return False


@db_conn(UserDatabaseConnection)
def add_user(DB_CONN, username: str) -> None:
    with DB_CONN:
        DB_CONN.add_user_into_db(username)
        DB_CONN.commit_changes()
