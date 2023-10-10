from flask import Flask, request, render_template, abort, session, redirect, url_for

from backend import FileSystem, DatabaseConnection2, Calculations
import SETTINGS

app = Flask(__name__)
env = SETTINGS.ENV
DB_CONN = DatabaseConnection2(SETTINGS.CONNECTION_DETAILS, env)
FS = FileSystem(SETTINGS.FINANCE_FILE_PATH / env)

@app.route('/api/update_new_receipts/<name>', methods = ['GET'])
def update_new_receipts(name):
    FS.setup(name)
    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    # pass recent receipt date to scraper container to scrape
    return redirect(f"http://{SETTINGS.IP_ADDRESS}:5000/api/scrape_everyday_rewards/{name}/{recent_date}/entry")
    # return redirect(f"http://{SETTINGS.IP_ADDRESS}:5050/api/insert_receipts_to_db")



@app.route('/api/insert_receipts_to_db')
def insert_receipts_to_db():
    # FS.setup('alex') 
    receipt_list = FS.get_receipt_names()
    for receipt in receipt_list:
        # process receipts to pandas df
        item_df = FS.receipt_to_dataframe(receipt) # consider this to make it the list of tuples needed - needs to be one receipt at a time
        receipt_date = FS.get_receipt_date(receipt)

        # upload to database
        with DB_CONN:
            DB_CONN.insert_receipt_into_receipt_table(receipt_date, FS.username, "receipt") # setting up the receipt_id as a variable in the postgres session env
            DB_CONN.insert_into_transactions(item_df)
            DB_CONN.commit_changes()

    FS.move_receipts()
    # delete tmp folder
    FS.delete_tmp()
    return redirect(url_for('update_weightings'))

# @app.route('/api/update_weightings', methods = ['GET', 'POST'])
# def update_weightings():
#     if request.method == 'POST':
#         weightings_dict = request.form
#         with DB_CONN:
#             weightings_df = DB_CONN.weightings_dict_to_df(weightings_dict)
#             DB_CONN.insert_weightings_into_table(weightings_df, env, "weightings")
#             DB_CONN.commit_changes()
#         return "done"  
#     with DB_CONN:
#         list_of_empty_weightings = DB_CONN.get_empty_weightings(env, "items_and_weightings")
    
#     return render_template('weightings_form.html', item_list=list_of_empty_weightings)

@app.route('/api/update_weightings', methods = ['GET', 'POST'])
def update_weightings():
    if request.method == 'POST':
        print(request.form)
    with DB_CONN:
        household_profile_list = DB_CONN.get_household_names('1') # session will log in and hold the profile_id
        list_of_null_weightings = DB_CONN.get_items_with_null_weightings('1') # session will log in and hold the profile_id
        list_of_persistent_weightings = DB_CONN.get_persistent_weightings_within_household('1')
    return render_template('weightings_form.html', profile_list = household_profile_list, item_list = list_of_null_weightings, persist_weights = list_of_persistent_weightings) # item_list = [eggs, bread, broc] profiles = [1,2,3] return = {eggs[1] : 0.1, eggs[2] : 0.3}


@app.route('/api/input_expenses/<occurence>', methods = ['GET', 'POST'])
def insert_one_off_costs(occurence): # occruence either 'one_off' or 'recurring'
    if request.method == 'POST':
        expenses_dict = request.form
        if 'id' in expenses_dict:
            with DB_CONN:
                DB_CONN.delete_expenses_row(expenses_dict, env, f"{occurence}_expenses")
                DB_CONN.commit_changes()
        else:
            with DB_CONN:
                DB_CONN.insert_expenses_into_table(expenses_dict, env, f"{occurence}_expenses")
                DB_CONN.commit_changes()
    with DB_CONN:
        data = DB_CONN.get_expenses_table(env, f"{occurence}_expenses")

    return render_template('expenses_form.html', data = data, occurence = occurence)


@app.route('/api/totals/dashboard')
def totals():
    with DB_CONN:
        expenses_table = DB_CONN.get_combined_expenses_as_df(env, "combined_expenses")
    
    calculations = Calculations(expenses_table)

    spent_tally = calculations.get_spent_tally()

    owings  = calculations.get_owes_tally()

    return render_template('totals.html', spent = spent_tally, owings=owings)

@app.route('/api/totals/confirm', methods = ['GET', 'POST'])
def confirm():
    return render_template('confirm.html')

@app.route('/api/totals/month_reset', methods = ['POST'])
def reset():
    # Archive current month spreadsheet into CSV
    with DB_CONN:
        all_expenses_df = DB_CONN.get_combined_expenses_as_df(env, "combined_expenses")
        

    FS.save_to_csv(all_expenses_df)

    # Delete all rows the current items_bought and one_off_costs tables
    with DB_CONN:
        DB_CONN.delete_from_table(env, "items_bought")
        DB_CONN.delete_from_table(env, "one_off_expenses")
        # Delete all weightings that are not persistent
        DB_CONN.delete_from_table(env, "weightings", where_cond="WHERE persist = false")
        DB_CONN.commit_changes()
    return redirect(url_for('totals'))