from flask import request, render_template, redirect, url_for, session, Blueprint
from .show_expenses import get_expenses_data
from .processing_expenses import remove_expenses_row, add_expenses_row
from .show_receipt_expenses import get_receipt_data
from ..user.views import needs_login

expenses_blueprint = Blueprint('expenses', __name__, template_folder="./templates")


@needs_login
@expenses_blueprint.route('/input/<occurence>', methods=['GET',])
def show_expenses_table_route(occurence):  # occruence either 'one_off' or 'recurring'
    data = get_expenses_data(occurence)
    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    return render_template('expenses_form.html',
                           data=data,
                           occurence=occurence,
                           household=household_names
                           )


@needs_login
@expenses_blueprint.route('/input/<occurence>', methods=['POST',])
def process_expenses_route(occurence):  # occruence either 'one_off' or 'recurring'
    expenses_dict = request.form
    if 'id' in expenses_dict:
        remove_expenses_row(expenses_dict)
    else:
        add_expenses_row(expenses_dict, occurence)

    target_url = url_for('expenses.show_expenses_table_route', occurence=occurence)
    return redirect(target_url)


@needs_login
@expenses_blueprint.route('/receipt', methods=['GET',])
def show_receipt_expenses_route():
    data = get_receipt_data()

    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    return render_template(
        'show_receipt_expenses.html',
        data=data,
        household=household_names)
