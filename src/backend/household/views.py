from flask import request, render_template, redirect, url_for, session,\
    Blueprint

from .exists_household import exists_household
from .create_new_household import create_new_household


blueprint = Blueprint('household', __name__, template_folder="./templates")


@blueprint.route('/', method=['GET',])
def join_or_create_route():
    return render_template('household.html')


@blueprint.route('/create_household', method=['GET',])
def create_household_route():
    return render_template('input_new_household_name.html')


@blueprint.route('/create_household', method=['POST',])
def add_new_household():
    household_name = request.form.get('household_name')
    if exists_household():
        return render_template('input_new_household_name.html')
    create_new_household(household_name)
    return redirect(url_for("household.assign_household_route"))


@blueprint.route('/join_household', method=['GET',])
def join_household_route():
    return render_template('input_existing_household_name.html')

@blueprint.route('/join_household', method=['POST',])
def assign_household_route():
    household_name = request.form.get('household_name')
    if not exists_household():
        return render_template('input_existing_household_name.html')
    assign_household(household_name)
    return ("Successfully Joined Household")
