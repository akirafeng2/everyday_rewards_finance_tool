from ..database import DatabaseConnection


class HouseholdDatabaseConnection(DatabaseConnection):
    def get_household_id(self, household: str) -> bool:
        """Returns household_id of given household_name"""
        query = """
        SELECT household_id 
        FROM household
        WHERE household_name = %s
        """
        self.conn.execute(query, (household,))
        result = self.cursor.fetchone()
        household_id = result[0]
        return household_id

    def insert_household(self, new_household: str) -> bool:
        """Adds given household into household table"""
        insert_statement = """
        INSERT INTO household (household_name)
        VALUES (%s)
        """
        self.conn.execute(insert_statement, (new_household))

    def update_profile_household
