import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import details
from ....src.backend.user.login import get_user_info, get_household_profiles


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.user.login.UserDatabaseConnection.get_user_info')
def test_get_user_info_valid(mock_db_conn: MagicMock, mock_connect: MagicMock, details: dict):
    """Unit test for when valid username password provided"""

    # Given
    # # Setting up Mock
    mock_db_conn.return_value = (
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


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.user.login.UserDatabaseConnection.get_user_info')
def test_get_user_info_invalid(mock_db_conn: MagicMock, mock_connect: MagicMock, details: dict):
    """Unit test for when invalid email password provided"""

    # Given
    # # Setting up Mock
    mock_db_conn.return_value = None

    # # Setting up expected result

    expected_result = None

    # When
    user_info = get_user_info(details.get('email'), details.get('password'))

    # Then
    assert user_info == expected_result


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.user.login.UserDatabaseConnection.get_household_names')
def test_get_household_profiles_in_household(mock_db_conn: MagicMock, mock_connect: MagicMock, details: dict):
    """Unit test to test output when user in a household"""

    # Given
    # # Setting up Mock
    mock_db_conn.return_value = [(4, 'alex'), (5, 'adam'), (6, 'tyler')]

    # # Setting up expected outcome
    expected_dict = {
        4: 'alex',
        5: 'adam',
        6: 'tyler'
    }

    # When
    household_names = get_household_profiles(details.get('user_id'))

    # Then
    assert household_names == expected_dict


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.user.login.UserDatabaseConnection.get_household_names')
def test_get_household_profiles_in_household(mock_db_conn: MagicMock, mock_connect: MagicMock, details: dict):
    """Unit test to test output when user not in a household"""

    # Given
    # # Setting up Mock
    mock_db_conn.return_value = []

    # # Setting up expected outcome
    expected_dict = {}

    # When
    household_names = get_household_profiles(details.get('user_id'))

    # Then
    assert household_names == expected_dict
