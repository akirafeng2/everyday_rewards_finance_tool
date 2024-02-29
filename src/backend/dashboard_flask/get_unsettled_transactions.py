from .database_actions import DashboardDatabaseConnection
from ..common import db_conn


@db_conn(DashboardDatabaseConnection)
def get_unsettled_transactions(DB_CONN: DashboardDatabaseConnection, user_id: str):
    with DB_CONN:
        transactions = DB_CONN.database_get_unsettled_transactions(user_id)
    print(transactions)

    return transactions
