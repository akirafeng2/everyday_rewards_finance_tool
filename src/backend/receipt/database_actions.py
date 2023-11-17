from ..database import DatabaseConnection
import pandas as pd


class ReceiptDatabaseConnection(DatabaseConnection):
    def insert_to_receipt_table(self, receipt_date: str, source: str) -> None:
        """Function to insert a given receipt_date, payer, and source into
        receipt table and also inserts the receipt_id into a the temp table
        new_receipt for later processing"""
        # setting up the receipt_id as a variable in the postgres session env
        insert_statement = """
        CREATE TEMP TABLE new_receipt (new_receipt_id INT);

        WITH inserted_row AS(
            INSERT INTO receipt (receipt_date, profile_id, source)
            VALUES (%s, %s, %s)
            RETURNING receipt_id
        )
        INSERT INTO new_receipt (new_receipt_id)
        SELECT receipt_id FROM inserted_row;
        """
        self.cursor.execute(
            insert_statement,
            (receipt_date, self.profile_id, source)
        )

    def insert_into_transactions(self, item_df: pd.DataFrame) -> None:
        """Function to insert the items from the list of tuples into
        transactions table. Uses the new_receipt_id from the
        insert_to_receipt_table method and also inserts item into the item
        table if it doens't already exist.
        Needs to run in the same session of insert_to_receipt_table as start
        of the function gets the item_df into right form for the executemany
        query"""

        item_df['item_dupe'] = item_df.loc[:, 'item']
        item_df = item_df[['item', 'item_dupe', 'price']]
        data_values = [tuple(row) for row in item_df.to_numpy()]

        insert_statement = """
        WITH ins AS(
            INSERT INTO item(item_name)
            VALUES (%s)
            ON CONFLICT (item_name) DO NOTHING
            RETURNING item_id
        )
        INSERT INTO transactions (item_id, receipt_id, price)
        VALUES (
            (
                SELECT item_id
                FROM ins
                UNION ALL
                SELECT item_id
                FROM item
                WHERE item_name = %s
            ),
            (
                SELECT MAX(new_receipt_id)
                FROM new_receipt
            ),
            %s
        );
        """

        self.cursor.executemany(insert_statement, data_values)
