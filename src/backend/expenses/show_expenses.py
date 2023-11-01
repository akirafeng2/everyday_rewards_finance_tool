from .database_actions import ExpensesDatabaseConnection
from ..database import db_conn


@db_conn(ExpensesDatabaseConnection)
def get_expenses_data(DB_CONN, occurence: str) -> list:
    """
    Function that returns the one off/recurring expenses in a pandas df
    """
    with DB_CONN:
        tuples = DB_CONN.get_expenses(occurence)
    return tuples
