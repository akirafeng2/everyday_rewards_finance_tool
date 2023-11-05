from flask import render_template, Blueprint
from ..user.views import needs_login
from .totals import get_totals

blueprint = Blueprint('dashboard', __name__, template_folder="./templates")


@blueprint.route('/', methods=['GET',])
@needs_login
def totals_route():

    spent_accumalated, owes = get_totals()

    return render_template(
        'totals.html',
        spent=spent_accumalated,
        owings=owes,
    )