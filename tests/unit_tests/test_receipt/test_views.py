from unittest.mock import patch, MagicMock
from ..common_fixtures import client


@patch('everyday_rewards_finance_tool.src.backend.receipt.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.receipt.views.get_file_system')
def test_latest_receipt_date_route(mock_get_file_system: MagicMock, mock_get_user_id: MagicMock, client):
    # Given
    mock_get_user_id.return_value = '1'
    mock_get_file_system.return_value.get_recent_receipt_date.return_value = '07Aug2023'

    # When
    response = client.get('/api/receipt/latest_receipt_date')

    # Then
    assert response.status_code == 200
    assert response.json == {'latest_receipt_date': '07Aug2023'}
    mock_get_file_system.assert_called_once_with('1')


@patch('everyday_rewards_finance_tool.src.backend.receipt.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.receipt.views.insert_receipt_to_db')
def test_insert_receipts_to_db_route(mock_insert: MagicMock, mock_get_user_id: MagicMock, client):
    # Given
    mock_get_user_id.return_value = '1'

    # When
    response = client.post('/api/receipt/insert_receipts_to_db')

    # Then
    assert response.status_code == 204
    mock_insert.assert_called_once_with('1')
