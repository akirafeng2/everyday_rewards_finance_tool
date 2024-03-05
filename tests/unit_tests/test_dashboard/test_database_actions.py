import pytest
from unittest.mock import patch
from ....src.backend.dashboard_flask.database_actions import DashboardDatabaseConnection
from ..common_fixtures import email, password, household, env, test_connection, user_id, household_id


@pytest.fixture
def dashboard_database_connection(test_connection: pytest.fixture, env: pytest.fixture):
    return DashboardDatabaseConnection(test_connection, env)


class TestDashboardDatabaseConnection:

    # tests
    @patch('psycopg2.connect')
    def test_database_get_unsettled_transactions(
        self,
        mock_connect,
        dashboard_database_connection: pytest.fixture,
        user_id: pytest.fixture
    ):
        """
        Test for the query to return the earliest date of a receipt
        in the household that is active/unsettled
        """
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up the query
        query_execute = """
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

        # When
        with dashboard_database_connection:
            dashboard_database_connection.database_get_unsettled_transactions(user_id)

        # Then
        mock_exe.assert_called_with(query_execute, (user_id,))

    @patch('psycopg2.connect')
    def test_database_get_paid_sum(
        self,
        mock_connect,
        dashboard_database_connection: pytest.fixture,
        user_id: pytest.fixture
    ):
        """
        Unittest of method to get sum of paid
        """
        # Given
        # # setting up the mock
        mock_exe = mock_connect.return_value.cursor.return_value.execute

        # # setting up the query
        query_execute = """
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

        # When
        with dashboard_database_connection:
            dashboard_database_connection.database_get_paid_sum(user_id)

        # Then
        mock_exe.assert_called_with(query_execute, (user_id,))
