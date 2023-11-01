from .database_actions import WeightingDatabaseConnection
from ..database import db_conn


@db_conn(WeightingDatabaseConnection)
def get_weightings_for_next_receipt(DB_CONN, receipt_id: str) -> dict:
    """
    takes in receipt_id as a string and returns a dict of length 2. The 0 index of the tuple is a list of
    non-persist items. the 1 index of the tuple is list of persist items
    """
    with DB_CONN:
        weightings_no_persistent_weights = DB_CONN.get_items_with_null_weightings_no_persistent_weights(receipt_id)
        weightings_with_persistent_weights = DB_CONN.get_items_with_null_weightings_with_persistent_weights(receipt_id)

    weightings_dict = {
        'item_list_no_persistent_weights': weightings_no_persistent_weights,
        'item_list_with_persistent_weights': weightings_with_persistent_weights
    }

    return weightings_dict
