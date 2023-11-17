from ..database import DatabaseConnection
import pandas as pd


class WeightingDatabaseConnection(DatabaseConnection):
    def get_new_receipts(self) -> list:
        """
        Returns a list of tuples. Each tuple is in the form (<receipt_id>, <receipt_date>) and represents receipts
        that have been added to transactions and have yet to been assigned weightings
        """
        select_statement = """
        SELECT DISTINCT receipt.receipt_id, receipt.receipt_date
        FROM transactions
        LEFT JOIN (
            SELECT *
            FROM receipt
            WHERE profile_id = %s
        ) as receipt ON transactions.receipt_id = receipt.receipt_id
        WHERE transactions.weighting_id is null
        """
        self.cursor.execute(select_statement, (self.profile_id,))
        result = self.cursor.fetchall()
        receipt_list = [(row[0], row[1]) for row in result]
        return receipt_list

    def update_transaction_persistence(self, transaction_id: str) -> None:
        """Updates the transactions table to override old weighting_id for a particular item in a household"""
        update_statement = """
        UPDATE transactions
        SET weighting_persist = False
        WHERE receipt_id in (
            SELECT receipt_id
            FROM receipt
            WHERE profile_id in (
                SELECT profile_id
                FROM profile
                WHERE household_id = (
                    SELECT household_id
                    FROM PROFILE
                    WHERE profile_id = %s
                )
            )
        )
        AND item_id = (
            SELECT item_id
            FROM transactions
            WHERE transaction_id = %s
            AND weighting_persist = True
        );

        UPDATE transactions
        SET weighting_persist = True
        WHERE transaction_id = %s;
        """
        self.cursor.execute(update_statement, (self.profile_id, transaction_id, transaction_id))

    def get_weighting_id(self, transaction_id: str) -> str:
        """
        Returns the weighting_id associated to a paticular transaction_id in the transactions table. If weighting_id
        does not yet exists, returns the next highest weighting_id number in the weightings table
        """

        query = """
        WITH NextAvailableWeighting AS (
            SELECT
                COALESCE(MAX(weighting_id) + 1, 1) AS next_weighting_id
            FROM weighting
        )
        SELECT
        CASE
            WHEN t.weighting_id IS NOT NULL THEN t.weighting_id
            ELSE n.next_weighting_id
        END AS final_weighting_id
        FROM transactions t
        LEFT JOIN NextAvailableWeighting n ON t.weighting_id IS NULL
        WHERE t.transaction_id = %s;
        """
        self.cursor.execute(query, (transaction_id,))
        result = self.cursor.fetchone()
        weighting_id = result[0]
        return weighting_id

    def insert_and_update_weighting(self, profile_id, weight: str, transaction_id: str) -> None:
        """Inserts entry into weighting table and updates transaction table with weighting_ID"""
        weighting_id = self.get_weighting_id(transaction_id)
        query = """
        INSERT INTO weighting
        VALUES (%s, %s, %s);

        UPDATE transactions
        SET weighting_id = %s
        WHERE transaction_id = %s;
        """
        self.cursor.execute(query, (weighting_id, profile_id, weight, weighting_id, transaction_id))

    def get_items_with_null_weightings_no_persistent_weights(self, receipt_id: int) -> list:
        """
        Returns a list of tuples of length two. tuple[0] is the transaction number of the item with no weighting,
        and tuple[1] is the item name
        """
        select_statement = """
        SELECT transactions.transaction_id, item.item_name
        FROM transactions
        LEFT JOIN item ON transactions.item_id = item.item_id
        LEFT JOIN (
            SELECT *
            FROM transactions
            WHERE weighting_persist = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE profile_id in (
                    SELECT profile_id
                    FROM profile
                    WHERE household_id = (
                        SELECT household_id
                        FROM PROFILE
                        WHERE profile_id = %s
                    )
                )
            )
        ) as household_persist_weight ON transactions.item_id = household_persist_weight.item_id
        WHERE transactions.weighting_id is null
        AND household_persist_weight.weighting_id is null
        AND transactions.receipt_id = %s;
        """
        self.cursor.execute(select_statement, (self.profile_id, receipt_id))
        result = self.cursor.fetchall()
        item_list = [(row[0], row[1]) for row in result]
        return item_list

    def get_items_with_null_weightings_with_persistent_weights(self, receipt_id: int) -> list:
        """
        Returns a list of tuples of length <household size> + 1 with weightings of each household member and item_id
        """
        select_statement = """
        SELECT transactions.transaction_id, item.item_name, profile.profile_id, MAX(weighting.weighting) as weighting
        FROM transactions
        LEFT JOIN item ON transactions.item_id = item.item_id
        LEFT JOIN (
            SELECT *
            FROM transactions
            WHERE weighting_persist = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE profile_id in (
                    SELECT profile_id
                    FROM profile
                    WHERE household_id = (
                        SELECT household_id
                        FROM PROFILE
                        WHERE profile_id = %s
                    )
                )
            )
        ) as household_persist_weight ON transactions.item_id = household_persist_weight.item_id
        INNER JOIN weighting ON household_persist_weight.weighting_id = weighting.weighting_id
        LEFT JOIN profile ON weighting.profile_id = profile.profile_id
        WHERE transactions.weighting_id is null
        AND transactions.receipt_id = %s
        GROUP BY (transactions.transaction_id, item.item_name, profile.profile_id)
        ORDER BY transactions.transaction_id, profile.profile_id
        """
        self.cursor.execute(select_statement, (self.profile_id, receipt_id))
        result = self.cursor.fetchall()

        # convert table from long to wide in Pandas
        column_names = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        df_wide = df.pivot(index=['transaction_id', 'item_name'], columns='profile_id', values='weighting')
        df_wide.reset_index(inplace=True)
        weighting_list = [tuple(row) for row in df_wide.to_numpy()]
        return weighting_list
