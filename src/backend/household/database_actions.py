from ..database import DatabaseConnection


class HouseholdDatabaseConnection(DatabaseConnection):
    def get_household_id(self, household: str) -> bool:
        """Returns household_id of given household_name"""
        query = """
        SELECT household_id
        FROM household
        WHERE household_name = %s
        """
        self.cursor.execute(query, (household,))
        result = self.cursor.fetchone()
        return result

    def insert_household(self, new_household: str) -> bool:
        """Adds given household into household table"""
        insert_statement = """
        INSERT INTO household (household_name)
        VALUES (%s)
        """
        self.cursor.execute(insert_statement, (new_household,))

    def update_profile_household(self, profile_id: str, household_id: str) -> None:
        """Updates given profile_id row in profile with household_id given"""
        update_statement = """
        UPDATE profile
        SET household_id = %s
        WHERE profile_id = %s
        """
        self.cursor.execute(update_statement, (household_id, profile_id))
