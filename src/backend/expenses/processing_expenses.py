from .database_actions import ExpensesDatabaseConnection
from ..database import db_conn
from werkzeug.datastructures import MultiDict
import datetime
from flask import session


@db_conn(ExpensesDatabaseConnection)
def remove_expenses_row(DB_CONN, remove_id_dict: MultiDict) -> None:
    remove_id = remove_id_dict.get('id')

    with DB_CONN:
        DB_CONN.deactivate_active_ind(remove_id)
        DB_CONN.commit_changes()


@db_conn(ExpensesDatabaseConnection)
def add_expenses_row(DB_CONN, expenses_row_dict: MultiDict, occurence: str) -> None:

    # variables for insert_expense_transactions
    item_name = expenses_row_dict.get('item')
    payer = expenses_row_dict.get('payer')
    price = expenses_row_dict.get('price')
    receipt_date = datetime.date.today()

    # setting up profile_weightings_tuples
    household_profile_list = session.get('household_profile_list')
    profile_weightings_tuples = []
    for profile in household_profile_list:
        profile_weightings_tuple = (profile[0], expenses_row_dict.get(profile[1]))
        profile_weightings_tuples.append(profile_weightings_tuple)

    with DB_CONN:
        DB_CONN.insert_expense_transactions(item_name, receipt_date, payer, occurence, price)
        DB_CONN.insert_expense_weightings(profile_weightings_tuples)
        DB_CONN.commit_changes()
