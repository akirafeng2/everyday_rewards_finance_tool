from .database_actions import ResetDatabaseConnection
from ..common import db_conn
from ..user.login import get_file_system


@db_conn(ResetDatabaseConnection)
def archive_month(DB_CONN: ResetDatabaseConnection, user_id: str) -> None:
    """
    function gets expenses df and saves it to csv in archive location
    """
    DB_CONN.profile_id = user_id
    with DB_CONN:
        all_expenses_df = DB_CONN.get_combined_expenses_as_df()

    get_file_system(user_id).save_to_csv(all_expenses_df)


@db_conn(ResetDatabaseConnection)
def deactivate_transactions(DB_CONN: ResetDatabaseConnection, user_id: str) -> None:
    """
    function calls database connection method to change all active transactions for household to inactive
    """
    DB_CONN.profile_id = user_id
    with DB_CONN:
        DB_CONN.deactivate_transactions()
        DB_CONN.commit_changes()
