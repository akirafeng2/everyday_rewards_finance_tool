from ..database import DatabaseConnection
import pandas as pd


class ResetDatabaseConnection(DatabaseConnection):
    def get_combined_expenses_as_df(self) -> pd.DataFrame:
        """
        Gets current active transactions and returns a dataframe
        """
        query = """
        SELECT
            t.transaction_id AS transaction_id,
            i.item_name AS item_name,
            t.price AS price,
            p.user_name as payer,
            r.source as source,
            w.weighting as weighting,
            r.receipt_date as date,
            p2.user_name as user_weighting
        FROM (
            SELECT *
            FROM transactions
            WHERE active_ind = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt as r
                WHERE profile_id in (
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
            index=['transaction_id', 'item_name', 'price', 'payer', 'source', 'date'],
            columns='user_weighting',
            values='weighting'
        )
        df_wide.reset_index(inplace=True)
        return df_wide

    def deactivate_transactions(self) -> None:
        """
        Changes all active_ind = T rows in transactions table for given household to false.
        Leaves recurring transactions as true
        """
        update_query = """
        UPDATE transactions
        SET active_ind = false
        WHERE transaction_id in (
            SELECT transaction_id
            FROM transactions
            WHERE active_ind = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt as r
                WHERE r.source != 'recurring'
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
        """
        self.cursor.execute(update_query, (self.profile_id,))
