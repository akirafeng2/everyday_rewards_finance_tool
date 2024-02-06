from flask import request, session, redirect, url_for, Blueprint, jsonify
from functools import wraps
from .. import SETTINGS
from . import login
from .add_user import add_profile


blueprint = Blueprint('user', __name__, template_folder='./templates')

env = SETTINGS.ENV


@blueprint.route('/register_profile', methods=['POST',])
def add_user_route():
    user_name = request.json.get('name')
    profile_id = request.json.get('user_id')
    add_profile(profile_id, user_name)
    return '', 204


@blueprint.route('/login_profile', methods=['POST'])
def login_user_route_post_response():
    user_id = request.json.get('user_id')
    login_info = login.get_user_info(user_id)
    login_info['household_profile_list'] = login.get_household_profiles(login_info['profile_id'])
    print(login_info)
    return jsonify(login_info)


# OLD vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def needs_login(func):  # needs to be deleted once all the old apis have beed replaced
    """Decorater to redirect to the login page if not logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('user.show_login_page_route'))
        if not session.get('household_id'):
            return redirect(url_for('household.join_or_create_route'))
        return func(*args, **kwargs)
    return wrapper
