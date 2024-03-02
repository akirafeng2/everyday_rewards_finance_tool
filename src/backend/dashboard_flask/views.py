from flask import Blueprint, jsonify
from ..common import verify_session_mod, get_user_id
from .get_unsettled_transactions import get_unsettled_transactions

blueprint = Blueprint('dashboard', __name__, template_folder="./templates")


@blueprint.route('/get_unsettled_transactions', methods=["GET",])
@verify_session_mod
def get_unsettled_transactions_route():
    user_id = get_user_id()
    try:
        transactions = get_unsettled_transactions(user_id)  # date should be the string it needs object
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 503
    else:
        return jsonify(transactions), 200
