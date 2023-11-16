from ..database import DatabaseConnection
import pandas as pd
from datetime import datetime


class ExpensesDatabaseConnection(DatabaseConnection):
    def get_expenses(self, occurrence: str, household_names: list) -> list:
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
            index=['transaction_id', 'item_name', 'price', 'payer'],
            columns='user_name',
            values='weighting'
        )
        df_wide.reset_index(inplace=True)
        weighting_list = [tuple(row) for row in df_wide.to_numpy()]

        # converting to dicts
        list_of_dict = []
        keys = [
            'id',
            'item',
            'price',
            'payer',
        ]
        keys.extend(household_names)
        for row in weighting_list:
            row_dict = dict(zip(keys, row))
            list_of_dict.append(row_dict)
        return list_of_dict

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
            VALUES (
                %s,
                (SELECT profile_id
                FROM profile
                WHERE user_name = %s),
                %s)
            RETURNING receipt_id
        )
        INSERT INTO transactions (item_id, receipt_id, price, weighting_id)
        VALUES (
            (
                SELECT item_id
                FROM ins_item
                UNION ALL
                SELECT item_id
                FROM item
                WHERE item_name = %s
            ),
            (
                SELECT receipt_id
                FROM ins_receipt
            ),
            %s,
            (
                SELECT next_weighting_id
                FROM temp_weighting
            )
        )
        """
        self.cursor.execute(insert_statement,
                            (item_name, receipt_date, payer, occurence, item_name, price)
                            )

    def insert_expense_weightings(self, profile_weightings_tuples: list) -> None:
        """
        Takes a list of tuples (<profile_id>, <weighting>) and inputs it into weightings db.
        Needs to be run after insert_expense_transactions as the temp_weighting temp table needs
        to be set up
        """
        insert_statement = """
        INSERT INTO weighting (weighting_id, profile_id, weighting)
        VALUES (
            (SELECT MAX(temp_weighting.next_weighting_id)
            FROM temp_weighting),
            %s,
            %s
            )
        """
        self.cursor.executemany(insert_statement, profile_weightings_tuples)

    def get_receipt_expenses(self, household_names: list):
        """
        Returns a list of dicts with expense line items
        (<transaction_id>, <item_name>, <price>, <payer>, <N weightings>)
        where N is number of people in the household
        """
        query = """
        SELECT
            t.transaction_id AS transaction_id,
            i.item_name AS item_name,
            t.price AS price,
            p.user_name as payer,
            w.weighting as weighting,
            r.receipt_date as date,
            p2.user_name as user_weighting
        FROM (
            SELECT *
            FROM transactions
            WHERE active_ind = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE source = 'receipt'
                AND profile_id in (
                    SELECT profile_id
                    FROM profile
                    WHERE household_id = (
                        SELECT household_id
                        FROM profile
                        WHERE profile_id = %s
                    )
                )
            )
        )
        AS t
        LEFT JOIN receipt AS r on t.receipt_id = r.receipt_id
        LEFT JOIN profile AS p on r.profile_id = p.profile_id
        LEFT JOIN item AS i on t.item_id = i.item_id
        LEFT JOIN weighting as w on t.weighting_id = w.weighting_id
        LEFT JOIN profile as p2 on w.profile_id = p2.profile_id
        ORDER BY t.transaction_id, w.profile_id
        """
        self.cursor.execute(query, (self.profile_id,))
        result = self.cursor.fetchall()

        # Convert table from long to wide in pandas
        column_names = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        df_wide = df.pivot(
            index=['transaction_id', 'item_name', 'price', 'payer', 'date'],
            columns='user_weighting',
            values='weighting'
        )
        df_wide.reset_index(inplace=True)
        weighting_list = [tuple(row) for row in df_wide.to_numpy()]

        # converting to dicts
        list_of_dict = []
        keys = [
            'transaction_id',
            'item',
            'price',
            'payer',
            'date'
        ]
        keys.extend(household_names)
        for row in weighting_list:
            row_dict = dict(zip(keys, row))
            list_of_dict.append(row_dict)
        return list_of_dict
