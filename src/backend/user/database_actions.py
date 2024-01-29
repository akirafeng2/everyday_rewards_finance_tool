from ..database import DatabaseConnection


class UserDatabaseConnection(DatabaseConnection):
    def get_user_info(self, user_email: str, hash_password: str) -> tuple:
        """With given user email and password, return a tuple
        (<profile_id>, <household_id>, <user_name>, <household_name>)
        Tuple will be empty if username or password is not correct
        """
        query = """
        SELECT
            profile.profile_id,
            profile.household_id,
            profile.user_name,
            household.household_name
        FROM profile
        LEFT JOIN household
        ON profile.household_id = household.household_id
        WHERE profile.user_email = %s
        AND profile.user_password = %s
        """
        self.cursor.execute(query, (user_email, hash_password))
        result = self.cursor.fetchone()
        return result

    def add_user_into_db(self, user_name: str) -> None:
        """adds a given user into the profiles table"""
        insert_statement = """
        INSERT INTO profile (user_name)
        VALUES (%s)
        """
        self.cursor.execute(insert_statement, (user_name,))

    def get_household_names(self, user_id: str) -> dict:
        """Returns the list names within a household"""
        select_statement = """
        SELECT profile_id, user_name
        FROM profile
        WHERE household_id = (
            SELECT household_id
            FROM profile
            WHERE profile_id = %s)
        ORDER BY profile_id
        """
        self.cursor.execute(select_statement, (user_id,))
        result = self.cursor.fetchall()
        household_names = {row[0]: row[1] for row in result}
        return household_names
