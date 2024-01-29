import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import details
from ....src.backend.user.login import get_user_info, get_household_profiles


@patch('database_actions.UserDatabaseConnection')
def test_get_user_info(mock_DB_CONN: MagicMock, details: dict):
    """Unit test tests whether this function correctly outputs the dictionary
    from the result given from the database connection"""

    # Given
    # # Setting up Mock
    mock_DB_get_user_info = mock_DB_CONN.return_value.get_user_info
    mock_DB_get_user_info.return_value = (
        details.get('user_id'),
        details.get('household_id'),
        details.get('username'),
        details.get('household_name')
    )

    # # Set Up Result
    expect_dict = {
        'profile_id': details.get('user_id'),
        'household_id': details.get('household_id'),
        'user_name': details.get('username'),
        'household_name': details.get('household_name')
    }
    # When
    user_info = get_user_info(
        details.get('email'),
        details.get('password')
    )

    # Then
    assert user_info == expect_dict
