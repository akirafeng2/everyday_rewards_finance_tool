from flask import session

from .database_actions import WeightingDatabaseConnection
from ..database import db_conn
from werkzeug.datastructures import MultiDict


@db_conn(WeightingDatabaseConnection)
def input_weightings_into_db(DB_CONN, weightings_dict: MultiDict) -> None:
    """Takes the multidict from the post request of the weightings_input route and inputs in the weightings into the database"""
    # input weighting data into database
    for weighting_identifier in weightings_dict:
        weight = weightings_dict[weighting_identifier]

        # Splitting '<profile_id>[<transaction_id>]'
        profile_id = weighting_identifier.split('[')[0]
        transaction_id = weighting_identifier.split('[')[1].strip(']')

        if profile_id == 'persist': # detects ('persist[2]', 'on') and means it is a persistent weighting indicator
            with DB_CONN:
                DB_CONN.update_transaction_persistence(transaction_id)
                DB_CONN.commit_changes()

        else:  # receives weightings in dict
            with DB_CONN:
                DB_CONN.insert_and_update_weighting(profile_id, weight, transaction_id)
                DB_CONN.commit_changes()

    session['receipt_counter'] += 1
