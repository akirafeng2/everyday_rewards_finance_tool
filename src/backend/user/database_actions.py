from ..database import DatabaseConnection


class UserDatabaseConnection(DatabaseConnection):
    def get_user_info(self, user_name: str) -> tuple:
        """With given username/user_name, return a tuple
        (<profile_id>, <household_id>, <user_name>, <household_name>)
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
        WHERE profile.user_name = %s
        """
        self.cursor.execute(query, (user_name,))
        result = self.cursor.fetchone()
        return result
