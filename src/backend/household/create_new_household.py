from .database_actions import HouseholdDatabaseConnection
from ..database import db_conn


@db_conn(HouseholdDatabaseConnection)
def create_new_household(DB_CONN, new_household_name: str) -> None:
    """Creates a new household in household table"""
    with DB_CONN:
        DB_CONN.insert_household(new_household_name)
        DB_CONN.commit_changes()
