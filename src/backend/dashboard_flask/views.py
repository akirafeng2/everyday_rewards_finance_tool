from flask import render_template, Blueprint, jsonify
from ..user.views import needs_login
from .totals import get_totals
from ..common import verify_session_mod, get_user_id
from .get_earliest_date import get_earliest_date

blueprint = Blueprint('home', __name__, template_folder="./templates")


@blueprint.route('/get_earliest_date', methods=["GET",])
@verify_session_mod
def get_earliest_date_route():
    user_id = get_user_id()
    date = get_earliest_date(user_id)  # date should be the string it needs object
    response = {"date": date}
    if date == "formaterror":
        return jsonify({'error': 'error retrieving date, possible date format issue'}), 400
    else:
        return jsonify(response)

# Old ------------------------------------------------------------------------------------


@blueprint.route('/', methods=['GET',])
@needs_login
def totals_route():

    spent_accumalated, owes = get_totals()

    return render_template(
        'totals.html',
        spent=spent_accumalated,
        owings=owes,
    )
