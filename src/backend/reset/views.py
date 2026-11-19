from flask import render_template, Blueprint, jsonify
from ..user.views import needs_login
from ..common import verify_session_mod, get_user_id
from .reset import archive_month, deactivate_transactions

blueprint = Blueprint('reset', __name__, template_folder="./templates")


@blueprint.route('/confirm', methods=['GET',])
@needs_login
def confirm_route():
    return render_template('confirm.html')


@blueprint.route('/month_reset', methods=['GET', 'POST'])
@verify_session_mod
def reset_route():
    user_id = get_user_id()
    try:
        # Archive current month's transactions into CSV, then mark them settled
        archive_month(user_id)
        deactivate_transactions(user_id)
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 503
    return '', 204
