from .file_system import FileSystem
from .SETTINGS import CONNECTION_DETAILS, FINANCE_FILE_PATH, ENV, STAGE
from functools import wraps

from flask import session, request

from supertokens_python.recipe.session.framework.flask import verify_session

import jwt


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


# def verify_session_mod(testing_config: bool):
#     if not testing_config:
#         def decorator(func):
#             @wraps(func)
#             @verify_session()
#             def wrapper(*args, **kwargs):
#                 return func(*args, **kwargs)
#             return wrapper
#         return decorator
#     else:
#         def decorator(func):
#             @wraps(func)
#             def wrapper(*args, **kwargs):
#                 return func(*args, **kwargs)
#             return wrapper
#         return decorator


def verify_session_mod(func):
    """
    Modifying supertokens verify_session decorator to not be called when the environement variable STAGE = TEST
    """
    if STAGE == "TEST":
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    else:
        @wraps(func)
        @verify_session()
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


def get_access_token():
    decoded = jwt.decode(request.cookies.get('sAccessToken'), options={"verify_signature": False})
    user_id = decoded.get('sub')
    return user_id
