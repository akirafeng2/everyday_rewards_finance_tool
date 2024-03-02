from .database_actions import DashboardDatabaseConnection
from ..common import db_conn


@db_conn(DashboardDatabaseConnection)
def get_unsettled_transactions(DB_CONN: DashboardDatabaseConnection, user_id: str):
    with DB_CONN:
        transactions = DB_CONN.database_get_unsettled_transactions(user_id)
    print(transactions)
    transactions_dict = {
        row[0]: {
            'item_name': row[1],
            'date': row[2].strftime("%d %B %Y"),
            'source': row[3],
            'payer': row[4],
            'cost': str(row[5])
        }
        for row in transactions
    }

    return transactions_dict
