import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client


@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_unsettled_transactions')
def test_get_earliest_date_route_valid_response(mock_get_transaction, mock_get_user_id, client):
    # Given
    # # Set up mock for the function
    mock_get_user_id.return_value = '1'
    mock_get_transaction.return_value = "27 January 2001"

    # # Set up expected results
    expected_result = {'date': "27 January 2001"}

    # When
    response = client.get('/api/dashboard/get_earliest_date')

    # Then
    assert response.status_code == 200
    assert response.json == expected_result


@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.dashboard_flask.views.get_unsettled_transactions')
def test_get_earliest_date_route_invalid_response(mock_get_transaction, mock_get_user_id, client):
    # Given
    # # set up mock for the function
    mock_get_user_id.return_value = '1'
    mock_get_transaction.return_value = "formaterror"
    # # Set up expected results
    expected_result = {'error': 'error retrieving date, possible date format issue'}

    # When
    response = client.get('/api/dashboard/get_earliest_date')

    # Then
    assert response.status_code == 400
