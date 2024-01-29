import pytest
import psycopg2
from unittest.mock import patch
from ...src.backend.database import DatabaseConnection
from .common_fixtures import username, household, env

test_connection_details = {
    "database": "test_db",
    "user": "test_user",
    "password": "test_password",
    "host": "localhost",
    "port": "5432"
}


@pytest.fixture
def database_connection(env):
    return DatabaseConnection(test_connection_details, env)


class TestDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_enter_method(self, mock_connect, database_connection, env):
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up search_path
        search_path_execute = "SET search_path TO %s;"
        # When
        with database_connection:
            # Then
            assert database_connection.conn is not None
            assert database_connection.cursor is not None
            mock_exe.assert_called_once_with(search_path_execute, (env,))

    @patch('psycopg2.connect')
    def test_exit_method_no_exception(self, mock_connect, database_connection):
        # Given
        mock_close = mock_connect.return_value.close

        # When
        with database_connection:
            pass

        # Then
        mock_close.assert_called_once_with()

    @patch('psycopg2.connect')
    def test_commit_changes(self, mock_connect, database_connection):
        # Test the commit_changes method
        # Given
        mock_commit = mock_connect.return_value.commit

        # When
        with database_connection:
            database_connection.commit_changes()

        # Then
        mock_commit.assert_called_once_with()
