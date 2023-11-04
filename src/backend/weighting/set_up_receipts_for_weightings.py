from flask import session

from .database_actions import WeightingDatabaseConnection
from ..common import db_conn


@db_conn(WeightingDatabaseConnection)
def set_up_receipts_for_weightings(DB_CONN: WeightingDatabaseConnection) -> None:
    with DB_CONN:
        session['receipts'] = DB_CONN.get_new_receipts()  # [(<receipt_id>, <receipt_date>), ...]
    session['num_of_receipts'] = len(session['receipts'])
    session['receipt_counter'] = 1
    print(session['receipts'])
