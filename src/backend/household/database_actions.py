from ..database import DatabaseConnection


class HouseholdDatabaseConnection(DatabaseConnection):
    def get_household_info(self, household_code: str) -> tuple:
        """Returns household_id and household_name given a code"""
        query = """
        SELECT household_id, household_name
        FROM household
        WHERE household_password = %s
        """
        self.cursor.execute(query, (household_code,))
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
