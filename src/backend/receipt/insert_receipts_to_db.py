from ..common import db_conn
from ..user.login import get_file_system
from .database_actions import ReceiptDatabaseConnection


@db_conn(ReceiptDatabaseConnection)
def insert_receipt_to_db(DB_CONN, user_id: str) -> None:
    """Method to insert receipts in the user's tmp folder
    in the file system and upload to database"""
    DB_CONN.profile_id = user_id
    FS = get_file_system(user_id)
    receipt_list = FS.get_receipt_names()
    for receipt in receipt_list:
        # process receipts to pandas df
        item_df = FS.receipt_to_dataframe(receipt)
        receipt_date = FS.get_receipt_date(receipt)

        # upload to database
        with DB_CONN:
            DB_CONN.insert_to_receipt_table(receipt_date, "receipt")
            DB_CONN.insert_into_transactions(item_df)
            DB_CONN.commit_changes()
        # move each committed receipt out of tmp so a retry can't insert it twice
        FS.move_receipt(receipt)

    # delete tmp folder
    FS.delete_tmp()
