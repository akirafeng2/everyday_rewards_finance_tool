from .database_actions import ExpensesDatabaseConnection
from ..database import db_conn
from werkzeug.datastructures import MultiDict


@db_conn(ExpensesDatabaseConnection)
def remove_expenses_row(DB_CONN, remove_id_dict: MultiDict) -> None:
    remove_id = remove_id_dict.get('id')

    with DB_CONN:
        DB_CONN.deactivate_active_ind(remove_id)
        DB_CONN.commit_changes()


@db_conn(ExpensesDatabaseConnection)
def add_expenses_row(DB_CONN, expenses_row_dict: MultiDict) -> None:
    pass
