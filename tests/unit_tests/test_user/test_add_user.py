import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import user_id, username
from ....src.backend.user.add_user import add_profile


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.user.login.UserDatabaseConnection.add_profile_into_db')
def test_add_profile(mock_db_conn: MagicMock, mock_connect: MagicMock, user_id: pytest.fixture,
                     username: pytest.fixture):
    """Unit test for add_profile function"""

    # Given

    # When
    value = add_profile(user_id, username)

    # Then
    mock_db_conn.assert_called_once_with(user_id, username)
    assert value is None
