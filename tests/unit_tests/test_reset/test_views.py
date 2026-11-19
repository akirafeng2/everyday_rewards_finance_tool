from unittest.mock import patch, MagicMock
from ..common_fixtures import client


@patch('everyday_rewards_finance_tool.src.backend.reset.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.reset.views.deactivate_transactions')
@patch('everyday_rewards_finance_tool.src.backend.reset.views.archive_month')
def test_reset_route_archives_and_deactivates(
    mock_archive: MagicMock, mock_deactivate: MagicMock, mock_get_user_id: MagicMock, client
):
    # Given
    mock_get_user_id.return_value = '1'

    # When
    response = client.post('/api/reset/month_reset')

    # Then
    assert response.status_code == 204
    mock_archive.assert_called_once_with('1')
    mock_deactivate.assert_called_once_with('1')


@patch('everyday_rewards_finance_tool.src.backend.reset.views.get_user_id')
@patch('everyday_rewards_finance_tool.src.backend.reset.views.archive_month')
def test_reset_route_database_offline(mock_archive: MagicMock, mock_get_user_id: MagicMock, client):
    # Given
    mock_get_user_id.return_value = '1'
    mock_archive.side_effect = ConnectionError('Postgres Database is Offline')

    # When
    response = client.post('/api/reset/month_reset')

    # Then
    assert response.status_code == 503
    assert response.json == {'error': 'Postgres Database is Offline'}
