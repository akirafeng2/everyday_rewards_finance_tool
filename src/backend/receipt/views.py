from flask import Flask, request, render_template, abort, session, redirect, url_for, Blueprint

from .. import SETTINGS
from ..file_system import fs
from ..user.views import needs_login
from .insert_receipts_to_db import insert_receipt_to_db


blueprint = Blueprint('receipt', __name__, template_folder='../templates')

@blueprint.route('/get_new_receipts', methods = ['GET',])
@needs_login
@fs
def get_new_receipts_route(FS):
    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    # pass recent receipt date to scraper conatiner to scrape
    return redirect(f"http://{SETTINGS.IP_ADDRESS}:5000/api/scrape_everyday_rewards/{session['household_name']}/{session['user_name']}/{recent_date}/entry")

@blueprint.route('/insert_receipts_to_db')
@needs_login
def insert_receipts_to_db_route():
    insert_receipt_to_db()
    return redirect(url_for('weightings.update_weightings_get_route'))


# @api.route('/api/insert_receipts_to_db')
# def insert_receipts_to_db():
#     DB_CONN = app.DB_CONN

#     receipt_list = FS.get_receipt_names()
#     for receipt in receipt_list:
#         # process receipts to pandas df
#         item_df = FS.receipt_to_dataframe(receipt) # consider this to make it the list of tuples needed - needs to be one receipt at a time
#         receipt_date = FS.get_receipt_date(receipt)

#         # upload to database
#         with DB_CONN:
#             DB_CONN.insert_receipt_into_receipt_table(receipt_date, "receipt") # setting up the receipt_id as a variable in the postgres session env
#             DB_CONN.insert_into_transactions(item_df)
#             DB_CONN.commit_changes()

#     FS.move_receipts()
#     # delete tmp folder
#     FS.delete_tmp()
#     return redirect(url_for('update_weightings'))