from ..database import DatabaseConnection
import pandas as pd


class DashboardDatabaseConnection(DatabaseConnection):
    def database_get_unsettled_transactions(self, profile_id: str) -> str:
        """
        Method to get the earliest date of a receipt
        in the household that is active/unsettled
        """
        query = """
        SELECT
            transactions.transaction_id as transaction_id,
            item.item_name as item_name,
            receipt.receipt_date as transaction_date,
            receipt.source as type,
            profile.user_name as paid,
            transactions.price as cost
        FROM transactions as transactions
        LEFT JOIN receipt as receipt ON transactions.receipt_id = receipt.receipt_id
        LEFT JOIN profile as profile ON receipt.profile_id = profile.profile_id
        LEFT JOIN item as item ON transactions.item_id = item.item_id
        WHERE active_ind = True
        AND profile.household_id = (
            select household.household_id
            from household as household
            left join profile as profile
            on household.household_id = profile.household_id
            where profile.profile_id = %s)
        ORDER by receipt_date desc
        """

        self.cursor.execute(query, (profile_id,))
        result = self.cursor.fetchall()
        return result

    def get_paid_list(self, profile_id: str) -> float:
        """
        Method to retrieve the spent list of each household member
        """
        query = """
        SELECT SUM(price)
        FROM (
            SELECT *
            FROM transactions
            WHERE active_ind = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
                WHERE profile_id = %s
                )
            ) AS t
        """
        self.cursor.execute(query, (profile_id,))
        result = self.cursor.fetchone()[0]
        if not result:
            result = 0
        print(result)
        return float(result)

    def get_accumalated_spend(self, profile_id: str) -> float:
        """
        Method to retrieve pandas data base of price, weighting, and weighting sum for the user in all active
        transactions in the household
        """
        query = """
        SELECT MAX(t.price) as price, w.weighting as weighting, MAX(s.weighting_total) as weighting_total
        FROM (
            SELECT *
            FROM transactions
            WHERE active_ind = true
            AND receipt_id in (
                SELECT receipt_id
                FROM receipt
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
        ) AS t
        LEFT JOIN weighting AS w ON t.weighting_id = w.weighting_id
        LEFT JOIN (
            SELECT weighting_id, SUM(weighting) as weighting_total
            FROM weighting
            GROUP BY weighting_id
        ) as s ON t.weighting_id = s.weighting_id
        GROUP BY t.transaction_id, w.profile_id, w.weighting
        HAVING w.profile_id = %s
        """
        self.cursor.execute(query, (self.profile_id, profile_id))
        result = self.cursor.fetchall()

        # convert table from long to wide in Pandas
        column_names = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(result, columns=column_names)
        accumalated_spend = round(df['weighting'] / df['weighting_total'] @ df['price'], 2)
        return float(accumalated_spend)
