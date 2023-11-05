from flask import request, render_template, session, redirect, url_for, Blueprint

from .set_up_receipts_for_weightings import set_up_receipts_for_weightings
from .input_weightings_into_db import input_weightings_into_db
from .get_weightings_for_next_receipt import get_weightings_for_next_receipt

from ..user.views import needs_login

weighting_blueprint = Blueprint('weighting', __name__, template_folder='./templates')


@weighting_blueprint.route('/update_receipt_weightings', methods=['GET',])
@needs_login
def update_weightings_get_route():
    set_up_receipts_for_weightings()
    return redirect(url_for('weighting.input_weightings_route'))


@weighting_blueprint.route('/update_receipt_weightings', methods=['POST',])
@needs_login
def update_weightings_post_route():
    # e.g. ImmutableMultiDict([('1[10]', '1'), ('2[10]', '1'), ('3[10]', '1'), ('1[2]', '1.00'), ('2[2]', '1.00'),
    # ('3[2]', '0.00'), ('persist[2]', 'on')]) where (<profile_id>[<transaction_id>], <weighting>)
    weightings_dict = request.form
    input_weightings_into_db(weightings_dict)
    print(session['receipts'])
    return redirect(url_for('weighting.input_weightings_route'))


@weighting_blueprint.route('/input_weightings', methods=['GET',])
@needs_login
def input_weightings_route():
    print(session['receipts'])
    try:
        current_receipt = session['receipts'].pop(0)
        session.modified = True
    except IndexError:
        return redirect(url_for('expenses.show_receipt_expenses_route'))
    print(session['receipts'])

    receipt_id = current_receipt[0]
    print(receipt_id)
    weighting_list_dict = get_weightings_for_next_receipt(receipt_id)

    return render_template(
        'weightings_form.html',
        profile_list=session['household_profile_list'],
        receipt_total=(session['receipt_counter'], session['num_of_receipts']),
        **weighting_list_dict
    )
