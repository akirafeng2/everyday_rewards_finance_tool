from flask import request, render_template, redirect, url_for, session, Blueprint

from .exists_household import exists_household
from .create_new_household import create_new_household
from .assign_household import assign_household

blueprint = Blueprint('household', __name__, template_folder="./templates")


@blueprint.route('/', methods=['GET',])
def join_or_create_route():
    return render_template('household.html', user_name=session.get('user_name'))


@blueprint.route('/create_household', methods=['GET',])
def create_household_route():
    return render_template('input_household_name.html', message='Input an Household Name')


@blueprint.route('/create_household', methods=['POST',])
def add_new_household():
    household_name = request.form.get('household_name')
    if exists_household(household_name):
        return render_template(
            'input_household_name.html',
            message='Household Name already Exists. Input a different Name'
        )
    create_new_household(household_name)
    return redirect(url_for("household.assign_household_route", household_name=household_name), code=307)


@blueprint.route('/join_household', methods=['GET',])
def join_household_route():
    return render_template('input_household_name.html', message='Input an Household Name')


@blueprint.route('/join_household', methods=['POST',])
def assign_household_route():
    household_name = request.values.get('household_name')
    if not exists_household(household_name):
        return render_template(
            'input_household_name.html',
            message='Household Name does not exist, please input another or create a new household'
        )
    assign_household(session.get('user_id'), household_name)
    return redirect(url_for('user.login_user_route', name=session.get('user_name')), code=307)
