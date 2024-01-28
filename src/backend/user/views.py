from flask import request, render_template, session, redirect, url_for, \
    Blueprint, jsonify
from functools import wraps
from .. import SETTINGS
from . import login
from .add_user import user_exists, add_user


blueprint = Blueprint('user', __name__, template_folder='./templates')

env = SETTINGS.ENV


# @blueprint.route('/login', methods=['GET',])
# def show_login_page_route():
#     return render_template("login.html")


@blueprint.route('/login', methods=['POST', 'OPTIONS'])
def login_user_route():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    else:
        login_email = request.json.get('email')
        login_password = request.json.get('password')
        login_info = login.get_user_info(login_email, login_password)
        if login_info is not None:
            login_info['household_profile_list'] = login.get_household_profiles()
            return jsonify(login_info)
        else:
            return jsonify({'error': 'Invalid email/password combination'}), 401

        # if login_info is not None:
        #     session['user_id'] = login_info[0]
        #     session['household_id'] = login_info[1]
        #     session['user_name'] = login_info[2]
        #     session['household_name'] = login_info[3]
        #     session['household_profile_list'] = login.get_household_profiles()
        #     session['logged_in'] = True
        #     return redirect(url_for("dashboard.totals_route"))
        # else:
        #     return redirect(url_for("user.register_user_route"))


@blueprint.route('/logout', methods=['GET',])
def logout_user_route():
    session.clear()
    return redirect(url_for('user.show_login_page_route'))


@blueprint.route('/register_user', methods=['GET',])
def register_user_route():
    return render_template("register_user.html")


@blueprint.route('/register_user', methods=['POST',])
def add_user_route():
    user_name = request.form['username']
    if user_exists(user_name):
        return render_template('user_exists.html')
    else:
        add_user(user_name)
        return render_template('user_added.html')


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
