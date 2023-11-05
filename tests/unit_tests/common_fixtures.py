import pytest


@pytest.fixture
def username():
    """sets the username used for FileSystem object"""
    return 'bob'


@pytest.fixture
def env():
    """sets the env used for FileSystem object"""
    return 'unit_test'


@pytest.fixture
def household():
    """sets the env used for FileSystem object"""
    return 'den'
