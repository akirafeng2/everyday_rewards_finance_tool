from flask import request, render_template, redirect, url_for, session, Blueprint
from .show_expenses import get_expenses_data
from .processing_expenses import remove_expenses_row, add_expenses_row
from ..user.views import needs_login
blueprint = Blueprint('expenses', __name__, template_folder="./templates")


@needs_login
@blueprint.route('/<occurence>', methods=['GET',])
def show_expenses_table_route(occurence):  # occruence either 'one_off' or 'recurring'
    data = get_expenses_data(occurence)
    household_names = [profile_info[1] for profile_info in session.get('household_profile_list')]
    return render_template('expenses_form.html',
                           data=data,
                           occurence=occurence,
                           household=household_names
                           )


@needs_login
@blueprint.route('/<occurence>', methods=['POST',])
def process_expenses_route(occurence):  # occruence either 'one_off' or 'recurring'
    expenses_dict = request.form
    if 'id' in expenses_dict:
        remove_expenses_row(expenses_dict)
    else:
        add_expenses_row(expenses_dict, occurence)

    target_url = url_for('expenses.show_expenses_table_route', occurence=occurence)
    return redirect(target_url)
