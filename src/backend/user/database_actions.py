from ..database import DatabaseConnection

class UserDatabaseConnection(DatabaseConnection):
    def get_user_info(self, nickname: str, household_name: str) -> tuple:
        """With given username/nickname and the user's household name, return a tuple (<profile_id>, <household_id>)"""
        query = """
        SELECT profile.profile_id, profile.household_id, profile.nickname, household.household_name 
        FROM profile
        LEFT JOIN household
        ON profile.household_id = household.household_id
        WHERE profile.nickname = %s
        AND household.household_name = %s
        """
        self.cursor.execute(query, (nickname, household_name))
        result = self.cursor.fetchone()
        return result