from flask import Flask, request, render_template, abort, session, redirect, url_for

from backend import FileSystem, DatabaseConnection
import SETTINGS

app = Flask(__name__)

FS = FileSystem(SETTINGS.FINANCE_FILE_PATH, SETTINGS.USERNAME)
DB_CONN = DatabaseConnection(SETTINGS.CONNECTION_DETAILS)

@app.route('/api/update_new_receipts', methods = ['GET'])
def update_new_receipts():
    
    # check for most recent receipt date

    # pass recent receipt date to scraper container to scrape

    # process receipts to pandas df
    item_df = FS.receipts_to_dataframe()

    # upload df to item df
    with DB_CONN:
        DB_CONN.insert_df_items_into_table(item_df, "household.items_bought")
        DB_CONN.commit_changes()
    
    # move receipts to year/month folder
    FS.move_receipts()
    # delete tmp folder
    return "done"