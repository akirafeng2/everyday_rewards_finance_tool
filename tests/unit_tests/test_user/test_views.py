import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client


@patch('everyday_rewards_finance_tool.src.backend.user.views.login.get_household_profiles')
@patch('everyday_rewards_finance_tool.src.backend.user.views.login.get_user_info')
def test_login_user_route_post_response_valid_user(mock_get_user_info: MagicMock,
                                                   mock_get_household_profiles: MagicMock,
                                                   client):
    """Tests json response when user is in database"""

    # Given
    # # Setting up Mocks
    mock_get_user_info.return_value = {
        'profile_id': 1,
        'household_id': 1,
        'user_name': "bob",
        'household_name': "Bobs House"
    }

    mock_get_household_profiles.return_value = {
        4: 'alex',
        5: 'adam',
        6: 'tyler'
    }

    # # Set up expected result
    expected_result = {
        'profile_id': 1,
        'household_id': 1,
        'user_name': 'bob',
        'household_name': 'Bobs House',
        'household_profile_list': {
            '4': 'alex',
            '5': 'adam',
            '6': 'tyler'
        }
    }

    # When
    response = client.post('/api/user/login', json={})

    # Then
    assert response.status_code == 200
    assert response.json == expected_result
