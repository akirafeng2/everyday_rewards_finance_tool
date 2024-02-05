import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import client, user_id, username


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
    response = client.post('/api/user/login_profile', json={})

    # Then
    assert response.status_code == 200
    assert response.json == expected_result


@patch('everyday_rewards_finance_tool.src.backend.user.views.add_profile')
def test_add_user_route(mock_add_profile, client, user_id, username):
    """Test react response for add_user_route api"""
    # Given
    
    # When
    response = client.post('/api/user/register_profile', json={
        'user_id': user_id,
        'username': username
    })

    # Then
    assert response.status_code == 204
    assert response.json is None
