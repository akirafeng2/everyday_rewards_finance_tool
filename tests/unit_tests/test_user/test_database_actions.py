import pytest
from unittest.mock import patch
from ....src.backend.user.database_actions import UserDatabaseConnection
from ..common_fixtures import email, password, household, env, test_connection, user_id


@pytest.fixture
def user_database_connection(test_connection: pytest.fixture, env: pytest.fixture):
    return UserDatabaseConnection(test_connection, env)


class TestUserDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_get_user_info(self, mock_connect, user_database_connection: pytest.fixture, email: pytest.fixture,
                           password: pytest.fixture):
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up the query
        query_execute = """
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

        # When
        with user_database_connection:
            user_database_connection.get_user_info(email, password)

        # Then
        mock_exe.assert_called_with(query_execute, (email, password))

    @patch('psycopg2.connect')
    def test_get_household_names(self, mock_connect,
                                 user_database_connection: pytest.fixture, user_id: pytest.fixture):
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up the query
        query_execute = """
        SELECT profile_id, user_name
        FROM profile
        WHERE household_id = (
            SELECT household_id
            FROM profile
            WHERE profile_id = %s)
        ORDER BY profile_id
        """

        # When
        with user_database_connection:
            user_database_connection.get_household_names(user_id)

        # Then
        mock_exe.assert_called_with(query_execute, (user_id,))
