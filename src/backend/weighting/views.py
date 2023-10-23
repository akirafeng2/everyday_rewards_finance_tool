from flask import Flask, request, render_template, abort, session, redirect, url_for, Blueprint

from .set_up_receipts_for_weightings import set_up_receipts_for_weightings
from .input_weightings_into_db import input_weightings_into_db
from .get_weightings_for_next_receipt import get_weightings_for_next_receipt

from ..user.views import needs_login

blueprint = Blueprint('weighting', __name__, template_folder='../templates')


@blueprint.route('/update_receipt_weightings', methods = ['GET',])
@needs_login
def update_weightings_get_route():
    set_up_receipts_for_weightings()
    return redirect(url_for('weighting.input_weightings_route'))


@blueprint.route('/update_receipt_weightings', methods = ['POST',])
@needs_login
def update_weightings_post_route():
    weightings_dict = request.form # e.g. ImmutableMultiDict([('1[10]', '1'), ('2[10]', '1'), ('3[10]', '1'), ('1[2]', '1.00'), ('2[2]', '1.00'), ('3[2]', '0.00'), ('persist[2]', 'on')]) where (<profile_id>[<transaction_id>], <weighting>)
    input_weightings_into_db(weightings_dict)
    print(session['receipts'])
    return redirect(url_for('weighting.input_weightings_route'))


@blueprint.route('/input_weightings', methods = ['GET',])
@needs_login
def input_weightings_route():
    print(session['receipts'])
    try:
        current_receipt = session['receipts'].pop(0)
        session.modified = True
    except IndexError:
        return "done"
    print(session['receipts'])

    receipt_id = current_receipt[0]
    print(receipt_id)
    weighting_list_dict = get_weightings_for_next_receipt(receipt_id)

    return render_template(
        'weightings_form.html', 
        profile_list = session['household_profile_list'], 
        receipt_total = (session['receipt_counter'], session['num_of_receipts']),
        **weighting_list_dict
        )

# @app.route('/api/update_weightings', methods = ['GET', 'POST'])
# def update_weightings():
#     # input weighting data into database
#     if request.method == 'POST':
#         weightings_dict = request.form # e.g. ImmutableMultiDict([('1[10]', '1'), ('2[10]', '1'), ('3[10]', '1'), ('1[2]', '1.00'), ('2[2]', '1.00'), ('3[2]', '0.00'), ('persist[2]', 'on')]) where (<profile_id>[<transaction_id>], <weighting>)
#         print(weightings_dict)
#         for weighting_identifier in weightings_dict:
#             weight = weightings_dict[weighting_identifier]
#             print(weighting_identifier)
#             # Splitting '<profile_id>[<transaction_id>]'
#             profile_id = weighting_identifier.split('[')[0]
#             transaction_id = weighting_identifier.split('[')[1].strip(']')
#             print(profile_id, transaction_id)
#             if profile_id == 'persist': # detects ('persist[2]', 'on') and means it is a persistent weighting indicator
#                 with DB_CONN:
#                     DB_CONN.update_transaction_persistence(transaction_id)
#                     DB_CONN.commit_changes()
            
#             else: # receives weightings in dict
#                 with DB_CONN:
#                     DB_CONN.insert_and_update_weighting(profile_id, weight, transaction_id)
#                     DB_CONN.commit_changes()

#         session['receipt_counter'] += 1
#     # set up receipts to have weighting assigned
#     elif request.method == 'GET':
#         with DB_CONN:
#             session['household_profile_list'] = DB_CONN.get_household_names() # session will log in and hold the profile_id
#             session['receipts'] = DB_CONN.get_new_receipts() # [(<receipt_id>, <receipt_date>), ...] 
#         session['num_of_receipts'] = len(session['receipts'])
#         session['receipt_counter'] = 1
#         print(session['receipts'])


#     # prepare transaction and weighting data for html
#     try:
#         current_receipt = session['receipts'].pop(0)
#     except IndexError:
#         session.clear()
#         return "done"
#     receipt_id = current_receipt[0]
#     with DB_CONN:
#         list_of_null_weightings_no_persistent_weights = DB_CONN.get_items_with_null_weightings_no_persistent_weights(receipt_id) # session will log in and hold the profile_id
#         list_of_null_weightings_with_persistent_weights = DB_CONN.get_items_with_null_weightings_with_persistent_weights(receipt_id)

#     return render_template(
#         'weightings_form.html', 
#         profile_list = session['household_profile_list'], 
#         item_list_no_persistent_weights = list_of_null_weightings_no_persistent_weights, 
#         item_list_with_persistent_weights = list_of_null_weightings_with_persistent_weights, 
#         receipt_total = (session['receipt_counter'], session['num_of_receipts'])
#         )