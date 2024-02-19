from flask import request, render_template, redirect, url_for, session, Blueprint, jsonify, g

from .exists_household import exists_household
from .create_new_household import create_new_household
from .assign_household import assign_household
from .get_household_info import get_household_info
from ..user.login import get_household_profiles

from supertokens_python.recipe.session.framework.flask import verify_session
from supertokens_python.recipe.session import SessionContainer

blueprint = Blueprint('household', __name__, template_folder="./templates")


@blueprint.route('/get_household_details', methods=['POST',])
@verify_session()
def get_household_details_route():
    household_code = request.json.get('household_code')
    household_info = get_household_info(household_code)
    if household_info is not None:
        return jsonify(household_info), 200
    else:
        return jsonify({'error': 'household_code'}), 403


@blueprint.route('/join_household', methods=['POST',])
@verify_session()
def join_household_route():
    session: SessionContainer = g.supertokens
    user_id = session.get_user_id()
    household_id = request.json.get('household_id')
    assign_household(user_id, household_id)
    response = {'household_profile_list': get_household_profiles(user_id)}
    print(response)
    return jsonify(response), 200

# OLD vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


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
