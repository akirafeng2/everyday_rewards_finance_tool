import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client, user_id, household_id, household_list


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
    assert response.status_code == 403
    assert response.json == expected_result


@patch('everyday_rewards_finance_tool.src.backend.household.views.assign_household')
@patch('everyday_rewards_finance_tool.src.backend.household.views.get_household_profiles')
def test_join_household_route_success(
    mock_get_household_profiles: MagicMock,
    mock_assign_household: MagicMock,
    user_id: pytest.fixture,
    household_id: pytest.fixture,
    household_list: pytest.fixture,
    client: pytest.fixture
):
    """
    Testing the /join_household route
    """
    # Given
    # # Setting up Mocks
    mock_get_household_profiles.return_value = household_list

    # # Setting up expected response
    expected_result = {
        'household_profile_list': {
            '1': 'Bob',
            '2': 'Bobby',
            '3': 'Bobbby'
        }
    }

    # When
    response = client.post('/api/household/join_household', json={
        'user_id': user_id,
        'household_id': household_id
    })

    # Then
    assert response.status_code == 200
    assert response.json == expected_result
