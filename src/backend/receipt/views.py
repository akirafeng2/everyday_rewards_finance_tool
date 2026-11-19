from flask import session, redirect, Blueprint, jsonify

from .. import SETTINGS
from ..common import fs, verify_session_mod, get_user_id
from ..user.login import get_file_system
from ..user.views import needs_login
from .insert_receipts_to_db import insert_receipt_to_db


blueprint = Blueprint('receipt', __name__, template_folder='../templates')


@blueprint.route('/get_new_receipts', methods=['GET',])
@needs_login
@fs
def get_new_receipts_route(FS):
    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    # pass recent receipt date to scraper conatiner to scrape
    return redirect(
        f"http://{SETTINGS.IP_ADDRESS}:5000/api/scrape_everyday_rewards/"
        f"{session['household_name']}/{session['user_name']}/"
        f"{recent_date}/entry"
    )


@blueprint.route('/latest_receipt_date', methods=['GET',])
@verify_session_mod
def latest_receipt_date_route():
    """Date of the user's most recently downloaded receipt, in the scraper's %d%b%Y format"""
    FS = get_file_system(get_user_id())
    return jsonify({'latest_receipt_date': FS.get_recent_receipt_date()}), 200


@blueprint.route('/insert_receipts_to_db', methods=['GET', 'POST'])
@verify_session_mod
def insert_receipts_to_db_route():
    try:
        insert_receipt_to_db(get_user_id())
    except ConnectionError as e:
        return jsonify({'error': str(e)}), 503
    return '', 204
