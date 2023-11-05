from .database_actions import DashboardDatabaseConnection
from ..common import db_conn
from flask import session


@db_conn(DashboardDatabaseConnection)
def get_totals(DB_CONN: DashboardDatabaseConnection):
    """Function to get spend total, return in the form of a list. one number for each member"""
    paid_list = []
    accumalated_list = []
    household_profiles = [profile_info[0] for profile_info in session.get('household_profile_list')]
    with DB_CONN:
        for profile_id in household_profiles:
            paid_list.append(DB_CONN.get_paid_list(profile_id))
            accumalated_list.append(DB_CONN.get_accumalated_spend(profile_id))

    owes_list = [a - b for a, b in zip(accumalated_list, paid_list)]

    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    accumalated_dict = dict(zip(household_names, accumalated_list))
    owes_dict = dict(zip(household_names, owes_list))
    return accumalated_dict, owes_dict
