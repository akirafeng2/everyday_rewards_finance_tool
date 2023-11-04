from .database_actions import ExpensesDatabaseConnection
from ..common import db_conn
from flask import session


@db_conn(ExpensesDatabaseConnection)
def get_expenses_data(DB_CONN, occurence: str) -> list:
    """
    Function that returns the one off/recurring expenses in a pandas df
    """
    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    with DB_CONN:
        tuples = DB_CONN.get_expenses(occurence, household_names)
    return tuples
