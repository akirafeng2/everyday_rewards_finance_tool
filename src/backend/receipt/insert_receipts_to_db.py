from ..database import db_conn
from ..file_system import fs
from .database_actions import ReceiptDatabaseConnection
from flask import session

@db_conn(ReceiptDatabaseConnection)
@fs
def insert_receipt_to_db(FS, DB_CONN) -> None:
    """Method to insert receipts in the user's tmp folder in the file system and upload to database"""
    receipt_list = FS.get_receipt_names()
    for receipt in receipt_list:
        # process receipts to pandas df
        item_df = FS.receipt_to_dataframe(receipt) # consider this to make it the list of tuples needed - needs to be one receipt at a time
        receipt_date = FS.get_receipt_date(receipt)

        # upload to database
        with DB_CONN:
            DB_CONN.insert_receipt_into_receipt_table(receipt_date, "receipt") # setting up the receipt_id as a variable in the postgres session env
            DB_CONN.insert_into_transactions(item_df)
            DB_CONN.commit_changes()

    FS.move_receipts()
    # delete tmp folder
    FS.delete_tmp()