from flask import Flask, request, session

def post(request: request, session: session) -> None:
    """"""
    user_details = request.form
    nickname = user_details[nickname]
    household_name = user_details[household_name]
    with DB_CONN:
        DB_CONN.get_user_profile_id()