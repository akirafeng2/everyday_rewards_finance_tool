from .database_actions import ResetDatabaseConnection
from ..database import db_conn
from ..file_system import fs, FileSystem


@db_conn(ResetDatabaseConnection)
@fs
def archive_month(FS: FileSystem, DB_CONN: ResetDatabaseConnection) -> None:
    """
    function gets expenses df and saves it to csv in archive location
    """
    with DB_CONN:
        all_expenses_df = DB_CONN.get_combined_expenses_as_df()

    FS.save_to_csv(all_expenses_df)


@db_conn(ResetDatabaseConnection)
def deactivate_transactions(DB_CONN: ResetDatabaseConnection) -> None:
    """
    function calls database connection method to change all active transactions for household to inactive
    """
    with DB_CONN:
        DB_CONN.deactivate_transactions()
        # DB_CONN.commit_changes()
