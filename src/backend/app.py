from flask import Flask, request, render_template, abort, session, redirect, url_for

from backend import FileSystem, DatabaseConnection
import SETTINGS

app = Flask(__name__)

FS = FileSystem(SETTINGS.FINANCE_FILE_PATH, SETTINGS.USERNAME)
DB_CONN = DatabaseConnection(SETTINGS.CONNECTION_DETAILS)

@app.route('/api/update_new_receipts', methods = ['GET'])
def update_new_receipts():

    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    # pass recent receipt date to scraper container to scrape
    return redirect(f"http://192.168.0.47:5000/api/scrape_everyday_rewards/{recent_date}/entry")


@app.route('/api/insert_receipts_to_db', methods = ['GET'])
def insert_receipts_to_db():
    # process receipts to pandas df
    item_df = FS.receipts_to_dataframe()

    # upload df to item db
    with DB_CONN:
        DB_CONN.insert_df_items_into_table(item_df, "household.items_bought")
        DB_CONN.commit_changes()
    
    # move receipts to year/month folder
    FS.move_receipts()
    # delete tmp folder
    FS.delete_tmp()
    return "done"