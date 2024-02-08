import pytest
from unittest.mock import patch, MagicMock
from ..common_fixtures import user_id, household_id
from ....src.backend.household.assign_household import assign_household


@patch('psycopg2.connect')
@patch('everyday_rewards_finance_tool.src.backend.household.'
       'assign_household.HouseholdDatabaseConnection.update_profile_household')
@patch('everyday_rewards_finance_tool.src.backend.household.'
       'assign_household.HouseholdDatabaseConnection.commit_changes')
def test_assign_household(
    mock_commit_changes: MagicMock,
    mock_update_profile_household: MagicMock,
    mock_connect: MagicMock,
    user_id: pytest.fixture,
    household_id: pytest.fixture
):
    """Unit forr assign_household and calling correct functions"""

    # Given

    # When
    assign_household(user_id, household_id)

    # Then
    mock_update_profile_household.assert_called_once_with(user_id, household_id)
    mock_commit_changes.assert_called_once
