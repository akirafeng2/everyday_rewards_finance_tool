from flask import request, render_template, session, redirect, url_for, \
    Blueprint
from functools import wraps
from .. import SETTINGS
from . import login
from .add_user import user_exists, add_user


blueprint = Blueprint('user', __name__, template_folder='../templates')

env = SETTINGS.ENV


@blueprint.route('/login', methods=['GET',])
def show_login_page_route():
    return render_template("login.html")


@blueprint.route('/login', methods=['POST',])
def login_user_route():
    login_dict = request.form

    login_info = login.get_user_info(login_dict)

    if login_info[0] is not None:
        session['user_id'] = login_info[0]
        session['household_id'] = login_info[1]
        session['user_name'] = login_info[2]
        session['household_name'] = login_info[3]
        session['logged_in'] = True
        return f"Successfull Login of \
            {session['user_name']}, {session['household_name']}"
    else:
        return redirect(url_for("user.register_user_route"))


@blueprint.route('/logout', methods=['GET',])
def logout_user_route():
    session.clear()
    return redirect(url_for('user.show_login_page_route'))


@blueprint.route('/register_user', methods=['GET',])
def register_user_route():
    return render_template("register_user")


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
