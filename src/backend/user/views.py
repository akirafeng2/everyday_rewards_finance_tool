from flask import Flask, request, render_template, abort, session, redirect, url_for, Blueprint
from functools import wraps
from .. import SETTINGS
from . import login


blueprint = Blueprint('user', __name__, template_folder='../templates')

env = SETTINGS.ENV

@blueprint.route('/login', methods = ['GET',])
def show_login_page():
    return render_template("login.html")

@blueprint.route('/login', methods = ['POST',])
def login_user():
    login_dict = request.form
    
    login_info = login.get_user_info(login_dict)
    
    if login_info is not None:
        session['user_id'] = login_info[0]
        session['household_id'] = login_info[1]
        session['user_name'] = login_info[2]
        session['household_name'] = login_info[3]
        session['logged_in'] = True
        return f"Successfull Login of {session['user_name']}, {session['household_name']}" # later on should go to totals dashboard
    else:
        return "User Not Found" # later needs to differentiate between new users and existing users without households
    

@blueprint.route('/logout', methods = ['GET',])
def logout_user():
    session.clear()
    return redirect(url_for('user.show_login_page'))

def needs_login(func):
    """Decorater to redirect to the login page if not logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('user.show_login_page'))
        return func(*args, **kwargs)
    return wrapper

# route for add user
# when I create a new user, the household needs to be UNASSIGNED
# route for join household
# route for 

