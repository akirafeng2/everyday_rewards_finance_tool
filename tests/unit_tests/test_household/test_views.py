import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client, user_id, household_id


@patch('everyday_rewards_finance_tool.src.backend.household.views.get_household_info')
def test_get_household_details_valid(
    mock_get_household_info: MagicMock,
    household_id,
    client: pytest.fixture
):
    """
    Testing the /get_household_details route when passed a valid household_code
    """
    # Given
    # # Setting up Mocks
    mock_get_household_info.return_value = {
        'household_id': 1,
        'household_name': "Bobs House"
    }

    # # Setting up expected result

    expected_result = {
        'household_id': 1,
        'household_name': "Bobs House"
    }

    # When
    response = client.post('/api/household/get_household_details', json={
        'household_code': household_id
    })

    # Then
    assert response.status_code == 200
    assert response.json == expected_result


@patch('everyday_rewards_finance_tool.src.backend.household.views.get_household_info')
def test_get_household_details_error(
    mock_get_household_info: MagicMock,
    household_id,
    client: pytest.fixture
):
    """
    Testing the /get_household_details route when passed a valid household_code
    """
    # Given
    # # Setting up Mocks
    mock_get_household_info.return_value = None

    # # Setting up expected result

    expected_result = {'error': 'household_code'}

    # When
    response = client.post('/api/household/get_household_details', json={
        'household_code': household_id
    })

    # Then
    assert response.status_code == 401
    assert response.json == expected_result
