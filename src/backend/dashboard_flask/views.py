from flask import Blueprint, jsonify

from ..common import verify_session_mod, get_user_id

from .get_unsettled_transactions import get_unsettled_transactions
from .get_owings import get_owings

blueprint = Blueprint('dashboard', __name__)


@blueprint.route('/get_unsettled_transactions', methods=["GET",])
@verify_session_mod
def get_unsettled_transactions_route():
    user_id = get_user_id()
    try:
        transactions = get_unsettled_transactions(user_id)
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 503
    else:
        return jsonify(transactions), 200


@blueprint.route('/get_owings', methods=["GET",])
@verify_session_mod
def get_owings_route():
    user_id = get_user_id()
    try:
        owings = get_owings(user_id)
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 503
    else:
        return jsonify(owings), 200
