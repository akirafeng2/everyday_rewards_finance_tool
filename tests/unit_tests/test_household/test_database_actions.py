import pytest
from unittest.mock import patch
from ....src.backend.household.database_actions import HouseholdDatabaseConnection
from ..common_fixtures import email, password, household, env, test_connection, user_id, household_id


@pytest.fixture
def household_database_connection(test_connection: pytest.fixture, env: pytest.fixture):
    return HouseholdDatabaseConnection(test_connection, env)


class TestHouseholdDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_get_household_info(self, mock_connect, household_database_connection: pytest.fixture,
                                household_id: pytest.fixture):
        """
        Test for the query to return household_info given the household_code.
        Household_id fixture used as substitute for hosuehold_code
        """
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up the query
        query_execute = """
        SELECT household_id, household_name
        FROM household
        WHERE household_password = %s
        """

        # When
        with household_database_connection:
            household_database_connection.get_household_info(household_id)

        # Then
        mock_exe.assert_called_with(query_execute, (household_id,))

    @patch('psycopg2.connect')
    def test_update_profile_household(self, mock_connect, household_database_connection: pytest.fixture,
                                      household_id: pytest.fixture, user_id: pytest.fixture):
        """
        Unit test for database action checking update_statement that assigns a household to a profile
        """
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # Setting up the statement
        insert_statement = """
        UPDATE profile
        SET household_id = %s
        WHERE profile_id = %s
        """

        with household_database_connection:
            household_database_connection.update_profile_household(household_id, user_id)

        # Then
        mock_exe.assert_called_with(insert_statement, (household_id, user_id))
