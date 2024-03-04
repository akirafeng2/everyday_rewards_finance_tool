from .database_actions import DashboardDatabaseConnection
from ..user.login import get_household_profiles
from ..common import db_conn


@db_conn(DashboardDatabaseConnection)
def get_owings(DB_CONN: DashboardDatabaseConnection, user_id):
    """Function to get spend total, return in the form of a list. one number for each member"""
    paid_list = []
    accumalated_list = []
    with DB_CONN:
        household_profiles = DB_CONN.get_household_profile_ids(user_id)
        for profile_id in household_profiles:
            paid_list.append(DB_CONN.database_get_paid_sum(profile_id))
            accumalated_list.append(DB_CONN.database_get_accumalated_spend_sum(profile_id))

    owes_list = [a - b for a, b in zip(accumalated_list, paid_list)]

    household_names = get_household_profiles(user_id)
    owes_dict = dict(zip(household_names, owes_list))
    return owes_dict
