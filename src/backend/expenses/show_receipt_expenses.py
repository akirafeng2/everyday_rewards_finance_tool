from .database_actions import ExpensesDatabaseConnection
from ..database import db_conn
from flask import session


@db_conn(ExpensesDatabaseConnection)
def get_receipt_data(DB_CONN: ExpensesDatabaseConnection) -> list:
    """
    Function that returns receipt expenses in key value pairs
    """
    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    with DB_CONN:
        dicts = DB_CONN.get_receipt_expenses(household_names)
    return dicts
