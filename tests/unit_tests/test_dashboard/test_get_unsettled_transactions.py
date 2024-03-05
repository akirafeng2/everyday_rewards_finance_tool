import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import user_id, household_id
from ....src.backend.dashboard_flask.get_unsettled_transactions import get_unsettled_transactions

from datetime import date
from decimal import Decimal


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.get_unsettled_transactions.'
       'DashboardDatabaseConnection.database_get_unsettled_transactions')
def test_get_unsettled_transactions_exists(
    mock_database_get_unsettled_transactions: MagicMock,
    mock_connect: MagicMock
):
    """
    Testing function when there is existing transctions returned from database
    """
    # Given
    # # Setting up Mock
    mock_database_get_unsettled_transactions.return_value = [
        (
            71,
            'Essentials Tomatoes Diced 400g',
            date(2023, 11, 11),
            'receipt',
            'alex',
            Decimal('3.88')
        ),
        (
            15,
            'Flying Goose Sriracha Sauce 455ml',
            date(2023, 10, 17),
            'receipt',
            'alex',
            Decimal('52.50')
        )
    ]

    # # Set up expected return value
    expected_transactions = [
        {
            'key': '71',
            'item_name': 'Essentials Tomatoes Diced 400g',
            'date': '11 November 2023',
            'source': 'receipt',
            'payer': 'Alex',
            'cost': '3.88'
        },
        {
            'key': '15',
            'item_name': 'Flying Goose Sriracha Sauce 455ml',
            'date': '17 October 2023',
            'source': 'receipt',
            'payer': 'Alex',
            'cost': '52.50'
        }
    ]
    # When
    transactions = get_unsettled_transactions("1")

    # Then
    assert transactions == expected_transactions


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.get_unsettled_transactions.'
       'DashboardDatabaseConnection.database_get_unsettled_transactions')
def test_get_unsettled_transactions_not_exists(
    mock_database_get_unsettled_transactions: MagicMock,
    mock_connect: MagicMock
):
    """
    Testing function when there is are no unsettled transactions from database
    """
    # Given
    # # Setting up Mock
    mock_database_get_unsettled_transactions.return_value = []

    # # Set up expected return value
    expected_result = []
    # When
    transactions = get_unsettled_transactions("1")

    # Then
    assert transactions == expected_result
