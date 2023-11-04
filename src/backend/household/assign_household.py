from .database_actions import HouseholdDatabaseConnection
from ..common import db_conn


@db_conn(HouseholdDatabaseConnection)
def assign_household(DB_CONN, profile_id: str, household_name: str) -> None:
    with DB_CONN:
        household_id = DB_CONN.get_household_id(household_name)
        DB_CONN.update_profile_household(profile_id, household_id)
        DB_CONN.commit_changes()


@db_conn(HouseholdDatabaseConnection)
def get_household_id(DB_CONN, household_name: str) -> str:
    with DB_CONN:
        household_id = DB_CONN.get_household_id(household_name)
    return household_id
