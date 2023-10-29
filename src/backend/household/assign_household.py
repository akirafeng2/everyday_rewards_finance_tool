from .database_actions import HouseholdDatabaseConnection
from ..database import db_conn


@db_conn(HouseholdDatabaseConnection)
def assign_household(DB_CONN, profile_id: str, household_id: str) -> None:
    with DB_CONN:
        DB_CONN.update_profile_housheold(profile_id, household_id)
