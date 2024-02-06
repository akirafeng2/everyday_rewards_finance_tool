from .database_actions import HouseholdDatabaseConnection
from ..common import db_conn


@db_conn(HouseholdDatabaseConnection)
def get_household_info(DB_CONN: HouseholdDatabaseConnection, household_code: str):
    """With a given household_code, retrieves household data from database including household_id and name"""
    with DB_CONN:
        household_info = DB_CONN.get_household_info(household_code)
    if household_info is not None:
        data_titles = ('household_id', 'household_name')
        household_info_dict = dict(zip(data_titles, household_info))
        return household_info_dict
    else:
        return None
