from flask import Flask, request, render_template, abort, session, redirect, url_for

from backend import FileSystem, DatabaseConnection
import SETTINGS

app = Flask(__name__)
DB_CONN = DatabaseConnection(SETTINGS.CONNECTION_DETAILS)
household = SETTINGS.ENV

@app.route('/api/update_new_receipts/<name>', methods = ['GET'])
def update_new_receipts(name):
    global FS
    
    FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / household, name)
    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    # pass recent receipt date to scraper container to scrape
    return redirect(f"http://{SETTINGS.IP_ADDRESS}:5000/api/scrape_everyday_rewards/{name}/{recent_date}/entry")
    # return redirect(f"http://{SETTINGS.IP_ADDRESS}:5050/api/insert_receipts_to_db")



@app.route('/api/insert_receipts_to_db', methods = ['GET', 'POST'])
def insert_receipts_to_db():
    if request.method == 'POST':
        weightings_dict = request.form
        with DB_CONN:
            weightings_df = DB_CONN.weightings_dict_to_df(weightings_dict)
            DB_CONN.insert_weightings_into_table(weightings_df, household, "weightings")
            DB_CONN.commit_changes()
        # move receipts to year/month folder
        FS.move_receipts()
        # delete tmp folder
        FS.delete_tmp()
        return "done"    

    # process receipts to pandas df
    item_df = FS.receipts_to_dataframe()

    # upload df to item db
    with DB_CONN:
        DB_CONN.insert_df_items_into_table(item_df, household, "items_bought")
        DB_CONN.commit_changes()
        list_of_empty_weightings = DB_CONN.get_empty_weightings(household, "items_and_weightings")
    
    return render_template('weightings_form.html', item_list=list_of_empty_weightings)
    