import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client


@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_unsettled_transactions')
def test_get_unsettled_transactions_route_valid_response(mock_get_transaction, client):
    # Given
    # # Set up mock for the function
    mock_get_transaction.return_value = {
        71: {
            'item_name': 'Essentials Tomatoes Diced 400g',
            'date': '11 November 2023',
            'source': 'receipt',
            'payer': 'alex',
            'cost': '3.88'
        },
        15: {
            'item_name': 'Flying Goose Sriracha Sauce 455ml',
            'date': '17 October 2023',
            'source': 'receipt',
            'payer': 'alex',
            'cost': '52.50'
        }
    }

    # # Set up expected results
    expected_response = {
        "71": {
            'item_name': 'Essentials Tomatoes Diced 400g',
            'date': '11 November 2023',
            'source': 'receipt',
            'payer': 'alex',
            'cost': '3.88'
        },
        "15": {
            'item_name': 'Flying Goose Sriracha Sauce 455ml',
            'date': '17 October 2023',
            'source': 'receipt',
            'payer': 'alex',
            'cost': '52.50'
        }
    }        

    # When
    response = client.get('/api/dashboard/get_unsettled_transactions')

    # Then
    assert response.status_code == 200
    assert response.json == expected_response


@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_unsettled_transactions')
def test_get_unsettled_transactions_route_invalid_response(mock_get_transaction, client):
    # Given
    # # set up mock for the function
    mock_get_transaction.side_effect = ConnectionError('Postgres Database is Offline')
    # # Set up expected results
    expected_result = {'error': 'Postgres Database is Offline'}

    # When
    response = client.get('/api/dashboard/get_unsettled_transactions')

    # Then
    assert response.status_code == 503
