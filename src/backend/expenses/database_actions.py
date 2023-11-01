from ..database import DatabaseConnection
import pandas as pd


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
