from flask import render_template, redirect, url_for, Blueprint
from ..user.views import needs_login
from .reset import archive_month, deactivate_transactions

reset_blueprint = Blueprint('reset', __name__, template_folder="./templates")


@reset_blueprint.route('/confirm', methods=['GET',])
@needs_login
def confirm_route():
    return render_template('confirm.html')


@reset_blueprint.route('/month_reset', methods=['GET',])
@needs_login
def reset_route():
    # Archive current month spreadsheet into CSV
    archive_month()

    # Delete all rows the current items_bought and one_off_costs tables
    deactivate_transactions()

    return redirect(url_for('dashboard.totals_route'))
