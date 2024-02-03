import pytest
from ...src.backend.app import app


@pytest.fixture
def client():
    """Create a test client for Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def details() -> dict:
    """sets a profile used for DatabaseConnection and FileSystem object"""
    details = {
        'user_id': 1,
        'username': 'bob',
        'household_id': 1,
        'household_name': 'bobs house',
        'password': 'password',
        'email': 'bob@test.com'
    }
    return details


@pytest.fixture
def username():
    """sets the username used for DatabaseConnection and FileSystem object"""
    return 'bob'


@pytest.fixture
def user_id():
    """sets the user_ID used for DatabaseConnection object"""
    return 1


@pytest.fixture
def email():
    """sets the username used for DatabaseConnection object"""
    return 'bob@test.com'


@pytest.fixture
def password():
    """sets the username used for DatabaseConnection object"""
    return 'password'


@pytest.fixture
def env():
    """sets the env used for DatabaseConnection and FileSystem object"""
    return 'unit_test'


@pytest.fixture
def household():
    """sets the env used for DatabaseConnection and FileSystem object"""
    return 'Bobs House'


@pytest.fixture
def household_id():
    """sets the env used for DatabaseConnection and FileSystem object"""
    return 1


@pytest.fixture
def test_connection():
    """sets the connection details use for DatabaseConnection object"""
    test_connection_details = {
        "database": "test_db",
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": "5432"
    }
    return test_connection_details
