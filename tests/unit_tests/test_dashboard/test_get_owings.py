import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import user_id, household_id
from ....src.backend.dashboard_flask.get_unsettled_transactions import get_unsettled_transactions


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.get_unsettled_transactions.'
       'DashboardDatabaseConnection.database_get_unsettled_transactions')
def test_get_owings(
    mock_database_get_unsettled_transactions: MagicMock,
    mock_connect: MagicMock
):
    """
    Testing function when there is existing transctions returned from database
    """