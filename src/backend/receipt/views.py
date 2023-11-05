from flask import session, redirect, url_for, Blueprint

from .. import SETTINGS
from ..common import fs
from ..user.views import needs_login
from .insert_receipts_to_db import insert_receipt_to_db


receipt_blueprint = Blueprint('receipt', __name__, template_folder='../templates')


@receipt_blueprint.route('/get_new_receipts', methods=['GET',])
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


@receipt_blueprint.route('/insert_receipts_to_db')
@needs_login
def insert_receipts_to_db_route():
    insert_receipt_to_db()
    return redirect(url_for('weighting.update_weightings_get_route'))
