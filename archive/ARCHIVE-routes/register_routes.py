from flask import Flask, request, render_template, abort, session, redirect, url_for, Blueprint
from flask import current_app as app
from .. import SETTINGS
import login



api = Blueprint('api', __name__, template_folder='../templates')

env = SETTINGS.ENV

@api.route('/login', methods = ['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        login_info = request.form
        user_name = login_info['username']
        household_name = login_info['household']
        login.post(user_name, hous, session)
        return "Successfull Login" # later on should go to totals dashboard


@api.route('/api/update_new_receipts/<name>', methods = ['GET'])
def update_new_receipts(name):
    FS.setup(name)
    # check for most recent receipt date
    recent_date = FS.get_recent_receipt_date()
    print(recent_date)
    # pass recent receipt date to scraper container to scrape
    return redirect(f"http://{SETTINGS.IP_ADDRESS}:5000/api/scrape_everyday_rewards/{name}/{recent_date}/entry")
    # return redirect(f"http://{SETTINGS.IP_ADDRESS}:5050/api/insert_receipts_to_db")



@api.route('/api/insert_receipts_to_db')
def insert_receipts_to_db():
    DB_CONN = app.DB_CONN

    receipt_list = FS.get_receipt_names()
    for receipt in receipt_list:
        # process receipts to pandas df
        item_df = FS.receipt_to_dataframe(receipt) # consider this to make it the list of tuples needed - needs to be one receipt at a time
        receipt_date = FS.get_receipt_date(receipt)

        # upload to database
        with DB_CONN:
            DB_CONN.insert_receipt_into_receipt_table(receipt_date, "receipt") # setting up the receipt_id as a variable in the postgres session env
            DB_CONN.insert_into_transactions(item_df)
            DB_CONN.commit_changes()

    FS.move_receipts()
    # delete tmp folder
    FS.delete_tmp()
    return redirect(url_for('update_weightings'))


@app.route('/api/update_weightings', methods = ['GET', 'POST'])
def update_weightings():
    # input weighting data into database
    if request.method == 'POST':
        weightings_dict = request.form # e.g. ImmutableMultiDict([('1[10]', '1'), ('2[10]', '1'), ('3[10]', '1'), ('1[2]', '1.00'), ('2[2]', '1.00'), ('3[2]', '0.00'), ('persist[2]', 'on')]) where (<profile_id>[<transaction_id>], <weighting>)
        print(weightings_dict)
        for weighting_identifier in weightings_dict:
            weight = weightings_dict[weighting_identifier]
            print(weighting_identifier)
            # Splitting '<profile_id>[<transaction_id>]'
            profile_id = weighting_identifier.split('[')[0]
            transaction_id = weighting_identifier.split('[')[1].strip(']')
            print(profile_id, transaction_id)
            if profile_id == 'persist': # detects ('persist[2]', 'on') and means it is a persistent weighting indicator
                with DB_CONN:
                    DB_CONN.update_transaction_persistence(transaction_id)
                    DB_CONN.commit_changes()
            
            else: # receives weightings in dict
                with DB_CONN:
                    DB_CONN.insert_and_update_weighting(profile_id, weight, transaction_id)
                    DB_CONN.commit_changes()

        session['receipt_counter'] += 1
    # set up receipts to have weighting assigned
    elif request.method == 'GET':
        with DB_CONN:
            session['household_profile_list'] = DB_CONN.get_household_names() # session will log in and hold the profile_id
            session['receipts'] = DB_CONN.get_new_receipts() # [(<receipt_id>, <receipt_date>), ...] 
        session['num_of_receipts'] = len(session['receipts'])
        session['receipt_counter'] = 1
        print(session['receipts'])


    # prepare transaction and weighting data for html
    try:
        current_receipt = session['receipts'].pop(0)
    except IndexError:
        session.clear()
        return "done"
    receipt_id = current_receipt[0]
    with DB_CONN:
        list_of_null_weightings_no_persistent_weights = DB_CONN.get_items_with_null_weightings_no_persistent_weights(receipt_id) # session will log in and hold the profile_id
        list_of_null_weightings_with_persistent_weights = DB_CONN.get_items_with_null_weightings_with_persistent_weights(receipt_id)

    return render_template(
        'weightings_form.html', 
        profile_list = session['household_profile_list'], 
        item_list_no_persistent_weights = list_of_null_weightings_no_persistent_weights, 
        item_list_with_persistent_weights = list_of_null_weightings_with_persistent_weights, 
        receipt_total = (session['receipt_counter'], session['num_of_receipts'])
        )


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