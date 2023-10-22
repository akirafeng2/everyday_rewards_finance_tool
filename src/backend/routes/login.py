from flask import Flask, request, session

def post(nickname: str, houshold_name: str, session: session) -> None:
    """Takes in user inputted nickname and household_name and assigns them to a given session"""
    with DB_CONN:
        user_details = DB_CONN.get_user_profile_id(nickname, houshold_name)

    session['profile_id'] = user_details[1]
    session['household_id'] = user_details[2]
    return session


