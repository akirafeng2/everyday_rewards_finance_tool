from .database_actions import HouseholdDatabaseConnection
from ..common import db_conn


@db_conn(HouseholdDatabaseConnection)
def exists_household(DB_CONN, household_name: str) -> bool:
    """Returns true/false if household exists/not exists"""
    with DB_CONN:
        household_id = DB_CONN.get_household_id(household_name)
        if household_id:
            return True
        else:
            return False
