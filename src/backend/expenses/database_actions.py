from ..database import DatabaseConnection
import pandas as pd
from datetime import datetime


class ExpensesDatabaseConnection(DatabaseConnection):
    def get_expenses(self, occurrence: str) -> list:
        """
        Returns a list of tuples with expense line items
        (<transaction_id>, <item_name>, <price>, <payer>, <N weightings>)
        where N is number of people in the household
        """
        query = """
        SELECT
            a.transaction_id AS transaction_id,
            a.item_name as item_name,
            a.price AS price,
            a.user_name AS payer,
            a.weighting AS weighting,
            b.user_name AS user_name
        FROM (
            SELECT
                transactions.transaction_id,
                item.item_name,
                transactions.price,
                profile.user_name,
                weighting.profile_id,
                weighting.weighting
            FROM transactions
            LEFT JOIN item ON transactions.item_id = item.item_id
            LEFT JOIN receipt ON transactions.receipt_id = receipt.receipt_id
            LEFT JOIN weighting ON transactions.weighting_id = weighting.weighting_id
            LEFT JOIN profile ON receipt.profile_id = profile.profile_id
            WHERE profile.household_id = (
                SELECT household_id
                FROM profile
                WHERE profile_id = %s)
            AND transactions.active_ind = True
            AND receipt.source = %s
        ) AS a
        LEFT JOIN profile AS b
        ON a.profile_id = b.profile_id
        """
        self.cursor.execute(query, (self.profile_id, occurrence))
        result = self.cursor.fetchall()

        # Convert table from long to wide in pandas
        column_names = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        df_wide = df.pivot(
            index=['transaction_id', 'price', 'item_name', 'payer'],
            columns='profile_id',
            values='weighting'
        )
        df_wide.reset_index(inplace=True)
        weighting_list = [tuple(row) for row in df_wide.to_numpy()]
        return weighting_list

    def deactivate_active_ind(self, transaction_id: str) -> None:
        """takes a given transaction_id and sets the active_ind to False"""
        update_statement = """
        UPDATE transactions
        SET active_ind = False
        WHERE transaction_id = %s
        """
        self.cursor.execute(update_statement, (transaction_id,))

    def insert_expense_transactions(self, item_name: str, receipt_date: datetime,
                                    payer: str, occurence: str, price: str) -> None:
        """
        takes attributes from expenses and inserts into transactions row and sets up next available weighting in
        a temp table
        """
        insert_statement = """
        CREATE TEMPORARY TABLE temp_weighting AS
        SELECT COALESCE(MAX(weighting_id) + 1, 1) AS next_weighting_id
        FROM weighting;

        WITH ins_item AS (
            INSERT INTO item (item_name)
            VALUES (%s)
            ON CONFLICT (item_name) DO NOTHING
            RETURNING item_id
        ),
        ins_receipt AS (
            INSERT INTO receipt (receipt_date, profile_id, source)
            VALUES (%s, %s, %s)
            RETURNING receipt_id

        INSERT INTO transactions (item_id, receipt_id, price, weighting_id)
        SELECT ins_item.item_id, ins_receipt.receipt_id, %s, temp_weighting.next_weighting_id;
        """
        self.cursor.execute(insert_statement, (item_name, receipt_date, payer, occurence, price))

    def insert_expense_weightings(self, profile_weightings_tuples: list) -> None:
        """
        Takes a list of tuples (<profile_id>, <weighting>) and inputs it into weightings db.
        Needs to be run after insert_expense_transactions as the temp_weighting temp table needs
        to be set up
        """
        insert_statement = """
        INSERT INTO weighting (weighting_id, profile_id, weighting)
        VALUES (temp_weighting.next_weighting_id, %s, %s)
        """
        self.cursor.executemany(insert_statement, profile_weightings_tuples)
