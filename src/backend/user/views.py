from flask import request, render_template, session, redirect, url_for, \
    Blueprint, jsonify
from functools import wraps
from .. import SETTINGS
from . import login
from .add_user import user_exists, add_profile


blueprint = Blueprint('user', __name__, template_folder='./templates')

env = SETTINGS.ENV


@blueprint.route('/register_profile', methods=['POST',])
def add_user_route():
    user_name = request.json.get('name')
    profile_id = request.json.get('user_id')
    add_profile(profile_id, user_name)
    return '', 204


@blueprint.route('/login', methods=['OPTIONS'])
def options_send_post():
    # Handle preflight request
    response = jsonify()
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


@blueprint.route('/login', methods=['POST'])
def login_user_route_post_response():
    login_email = request.json.get('email')
    login_password = request.json.get('password')
    login_info = login.get_user_info(login_email, login_password)
    if login_info is not None:
        login_info['household_profile_list'] = login.get_household_profiles(login_info['profile_id'])
        print(login_info)
        return jsonify(login_info)
    else:
        return jsonify({'error': 'Invalid email/password combination'}), 401

# OLD vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


@blueprint.route('/logout', methods=['GET',])
def logout_user_route():
    session.clear()
    return redirect(url_for('user.show_login_page_route'))


def needs_login(func):
    """Decorater to redirect to the login page if not logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('user.show_login_page_route'))
        if not session.get('household_id'):
            return redirect(url_for('household.join_or_create_route'))
        return func(*args, **kwargs)
    return wrapper

# when I create a new user, the household needs to be UNASSIGNED
# route for join household
# route for
