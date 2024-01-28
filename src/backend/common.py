from .file_system import FileSystem
from .SETTINGS import CONNECTION_DETAILS, FINANCE_FILE_PATH, ENV
from functools import wraps

from flask import session


def db_conn(db_class):
    """decorator to instantiate a DatabaseConnection and pass it into the local env of a function"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = db_class(CONNECTION_DETAILS, ENV)
            return func(instance, *args, **kwargs)
        return wrapper
    return decorator


def fs(func):
    """decorator to instantiate a DatabaseConnection and pass it into the local env of a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = FileSystem(FINANCE_FILE_PATH, ENV, session['user_name'], session['household_name'])
        return func(instance, *args, **kwargs)
    return wrapper
